from datetime import datetime as dt
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

#Datetime para o nome do arquivo

def get_video_id(url):
    # Extrai o ID do vídeo do link do YouTube
    video_id = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if video_id:
        return video_id.group(1)
    else:
        raise ValueError("URL inválida")
    
def get_transcript(video_id):
    # Obtém a transcrição do vídeo
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Tentar obter transcrição gerada manualmente
        transcript = None
        for transcript_obj in transcript_list:
            if not transcript_obj.is_generated:
                transcript = transcript_obj.fetch()
                break
        # Caso não exista transcrição manual, obter a gerada automaticamente
        if transcript is None:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
    except Exception as e:
        raise Exception(f"Erro ao obter transcrição: {e}")
    
    return transcript

def main():
    url = input("Digite o link do vídeo do YouTube: ")
    try:
        video_id = get_video_id(url)
        transcript = get_transcript(video_id)

        # Obter o diretório atual
        current_dir = os.getcwd()

        # Criar um diretório para salvar os arquivos de transcrição
        save_dir = os.path.join(current_dir, "transcripts")
        os.makedirs(save_dir,exist_ok=True)

        # Gerar um nome único para o arquivo atual
        now = dt.now().strftime("%d%m%Y-%H%M%S")
        filename = f"transcript_{now}.txt"
        file_path = os.path.join(save_dir, filename)

        # Salvar a transcrição no arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(f"{entry['start']} : {entry['text']}\n")
            
        print(f"Transcrição salva em {file_path}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
