# -*- coding: utf-8 -*-
import os
import sys
import io
import json
import re
from datetime import datetime

# Set standard output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_transcript_path():
    app_data = os.path.expanduser(r'~/.gemini/antigravity/brain')
    conv_id = '03ba4400-054c-4ed5-9e67-8d4f83c000c0'
    transcript_path = os.path.join(app_data, conv_id, '.system_generated', 'logs', 'transcript_full.jsonl')
    if not os.path.exists(transcript_path) and os.path.exists(app_data):
        for folder in os.listdir(app_data):
            candidate = os.path.join(app_data, folder, '.system_generated', 'logs', 'transcript_full.jsonl')
            if os.path.exists(candidate):
                return candidate
    return transcript_path

def sync_prompt_logs():
    transcript_path = get_transcript_path()
    if not os.path.exists(transcript_path):
        print('Transcript file not found:', transcript_path)
        return

    prompts = []
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except Exception:
                continue
            if data.get('type') == 'USER_INPUT':
                content = data.get('content', '')
                req_match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', content, re.DOTALL)
                time_match = re.search(r'The current local time is:\s*([0-9T:+-]+)', content)
                
                req_text = req_match.group(1).strip() if req_match else content.strip()
                if time_match:
                    try:
                        dt = datetime.fromisoformat(time_match.group(1))
                        timestamp_str = dt.strftime('%d-%m-%Y %H:%M:%S')
                    except Exception:
                        timestamp_str = time_match.group(1)
                else:
                    timestamp_str = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                
                prompts.append((timestamp_str, req_text))

    fence = chr(96) * 3
    lines = ['# Lịch sử Prompt Tương tác AI (Prompt Log)\n']
    for ts, prompt in prompts:
        # Mask GitHub personal access tokens to protect credentials and pass push protection
        masked_prompt = re.sub(r'ghp_[A-Za-z0-9_]{20,}', 'ghp_************************************ (GitHub Personal Access Token)', prompt)
        lines.append(f'### [{ts}] | Gemini')
        lines.append(fence + 'text')
        lines.append(masked_prompt)
        lines.append(fence)
        lines.append('')
        lines.append('---')
        lines.append('')

    with open('promt_log.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Successfully synchronized {len(prompts)} prompts to promt_log.md in UTF-8.')

if __name__ == '__main__':
    sync_prompt_logs()
