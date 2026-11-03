#!/usr/bin/env python3
"""Opt-in QLoRA specialist training. Requires a local GPU and installed ML extras."""
import argparse
import json
from pathlib import Path

import specialists

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--specialist",required=True)
    p.add_argument("--train",type=Path,required=True,help="Curated JSONL; no eval/holdout examples")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--epochs",type=int,default=2)
    p.add_argument("--max-length",type=int,default=1024)
    p.add_argument("--base-model",help="Local full-weight HF checkpoint path or cached HF ID (GGUF/Ollama not supported)")
    p.add_argument("--allow-download",action="store_true",help="Explicit permission for HF model downloads")
    args=p.parse_args()
    spec=specialists.registry()["specialists"].get(args.specialist)
    if not spec: p.error("Unknown specialist")
    if args.epochs<1 or args.epochs>8: p.error("Epochs must be 1-8")
    from datasets import Dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments, Trainer
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    import torch
    if not torch.cuda.is_available(): p.error("QLoRA training requires CUDA; no CPU fallback")
    samples=[json.loads(line) for line in args.train.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not samples or any(not isinstance(s.get("case_id"),str) or
        not isinstance(s.get("prompt"),str) or not isinstance(s.get("completion"),str) for s in samples):
        p.error("Expected curated JSONL rows: case_id, prompt, completion")
    if len({s["case_id"] for s in samples})!=len(samples): p.error("Duplicate training case IDs")
    base=args.base_model or specialists.registry()["base_model"]["huggingface"]
    if not args.allow_download and args.base_model and not Path(base).is_dir():
        p.error("--base-model must be a local Hugging Face checkpoint folder unless --allow-download is explicitly given")
    tokenizer=AutoTokenizer.from_pretrained(base,local_files_only=not args.allow_download)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(
        base,quantization_config=quant,device_map="auto",local_files_only=not args.allow_download)
    model.config.use_cache=False
    model=prepare_model_for_kbit_training(model)
    model=get_peft_model(model,LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,
        bias="none",task_type="CAUSAL_LM",target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]))
    def tokenize(row):
        system=("You are a qualified PMX Blender stage construction specialist. "
                "Return only JSON with target, code, explanation; do not assume stage acceptance."
                if spec["kind"]=="stage_candidate"
                else "You are a narrow PMX Blender Python helper. Return JSON with target, code, explanation.")
        prompt=tokenizer.apply_chat_template([
            {"role":"system","content":system},
            {"role":"user","content":row["prompt"]}],tokenize=False,add_generation_prompt=True)
        full=prompt+row["completion"]+tokenizer.eos_token
        encoded=tokenizer(full,truncation=True,max_length=args.max_length)
        prefix=tokenizer(prompt,add_special_tokens=False)["input_ids"]
        encoded["labels"]=[-100]*min(len(prefix),len(encoded["input_ids"]))+encoded["input_ids"][len(prefix):]
        return encoded
    ds=Dataset.from_list(samples).map(tokenize,remove_columns=list(samples[0].keys()))
    def collate(features):
        # Pad supervised completion labels with -100, not EOS. Never train on user prompts.
        import torch
        width=max(len(x["input_ids"]) for x in features)
        batch={}
        for key in ("input_ids","attention_mask","labels"):
            fill=-100 if key=="labels" else (tokenizer.pad_token_id if key=="input_ids" else 0)
            batch[key]=torch.tensor([x[key]+[fill]*(width-len(x[key])) for x in features],dtype=torch.long)
        return batch
    args.output.mkdir(parents=True,exist_ok=True)
    ta=TrainingArguments(output_dir=str(args.output/"checkpoints"),
        num_train_epochs=args.epochs,per_device_train_batch_size=1,
        gradient_accumulation_steps=8,learning_rate=1e-4,logging_steps=10,
        save_strategy="epoch",report_to="none",fp16=True,gradient_checkpointing=True)
    trainer=Trainer(model=model,args=ta,train_dataset=ds,
        data_collator=collate)
    trainer.train()
    model.save_pretrained(args.output/"adapter")
    tokenizer.save_pretrained(args.output/"adapter")
    print("Saved adapter; NOT QUALIFIED. Independently evaluate held-out cases and explicitly promote.")

if __name__=="__main__":main()
