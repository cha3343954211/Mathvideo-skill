"""
voxcpm_batch.py: 本地 VoxCPM2 离线神经语音生成工具 (Intel Arc B580 加速)
支持单条或批量文本合成，生成 48kHz 超高保真播音级沉稳解说音频。
"""
import sys
import os
import json
import time
import hashlib
import argparse
from pathlib import Path

VOXCPM_VENV_PYTHON = r"D:\AIworks\TTS\.venv311\Scripts\python.exe"
VOXCPM_MODEL_DIR = r"D:\AIworks\TTS\VoxCPM\pretrained_models\VoxCPM2"
DEFAULT_VOICE_DESIGN = "(四十岁上下的男性，嗓音低沉浑厚，气息沉稳，数学纪录片旁白)"


def synthesize_batch(items, output_dir, device="xpu", voice_design=DEFAULT_VOICE_DESIGN, ref_wav=None):
    """
    items: list of (key, text)
    """
    import soundfile as sf
    from voxcpm import VoxCPM

    out_p = Path(output_dir)
    out_p.mkdir(parents=True, exist_ok=True)

    print(f"[VoxCPM] 正在加载模型权重到 {device}... ({VOXCPM_MODEL_DIR})", file=sys.stderr)
    t0 = time.time()
    model = VoxCPM.from_pretrained(VOXCPM_MODEL_DIR, load_denoiser=False, device=device)
    sr = model.tts_model.sample_rate
    print(f"[VoxCPM] 模型装载完成，耗时 {time.time() - t0:.1f}s，采样率 {sr}Hz", file=sys.stderr)

    results = {}
    for key, text in items:
        out_file = out_p / f"{key}.wav"
        if out_file.exists() and out_file.stat().st_size > 0:
            dur = len(sf.read(str(out_file))[0]) / sr
            results[key] = (str(out_file), dur)
            print(f"[VoxCPM] 命中缓存: {key} ({dur:.2f}s)", file=sys.stderr)
            continue

        full_prompt = f"{voice_design}{text}" if voice_design else text
        gen_kwargs = {
            "text": full_prompt,
            "cfg_value": 2.0,
            "inference_timesteps": 10,
            "seed": 108
        }
        if ref_wav and Path(ref_wav).exists():
            gen_kwargs["reference_wav_path"] = str(Path(ref_wav).resolve())
            print(f"[VoxCPM] 挂载参考音色克隆: {ref_wav}", file=sys.stderr)

        t_start = time.time()
        wav = model.generate(**gen_kwargs)
        elapsed = time.time() - t_start
        dur = len(wav) / sr
        sf.write(str(out_file), wav, sr)
        results[key] = (str(out_file), dur)
        print(f"[VoxCPM] 合成完毕: '{text[:20]}...' -> {dur:.2f}s (耗时 {elapsed:.2f}s, RTF={elapsed/dur:.3f})", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_in", type=str, required=True, help="输入 JSON 文件，格式为 [{'key': '...', 'text': '...'}]")
    parser.add_argument("--json_out", type=str, required=True, help="输出元信息 JSON")
    parser.add_argument("--out_dir", type=str, required=True, help="音频输出目录")
    parser.add_argument("--voice_design", type=str, default=DEFAULT_VOICE_DESIGN, help="声音设计 Prompt")
    parser.add_argument("--ref_wav", type=str, default=None, help="参考克隆音频路径")
    args = parser.parse_args()

    with open(args.json_in, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = [(d["key"], d["text"]) for d in data]
    res = synthesize_batch(items, args.out_dir, voice_design=args.voice_design, ref_wav=args.ref_wav)

    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print("[VoxCPM] 全部任务执行完毕！", file=sys.stderr)


if __name__ == "__main__":
    main()
