import torch, whisper

# Check detailed information on: https://github.com/openai/whisper#python-usage

def SpeechToText(audio, model):
    # Note: Used ffmpeg-read audio input instead of path
    # (client input is not a voice, it is a AudioBlob.)
    # audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)

    # decode the audio
    options = whisper.DecodingOptions(fp16=torch.cuda.is_available())
    result = whisper.decode(model, mel, options)
    
    return {'language': max(probs, key=probs.get), 'result': result.text}
