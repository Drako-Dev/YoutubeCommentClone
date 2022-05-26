from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_apis import create_service
import time
import os

API_KEY = ""

def getVideoComments(videoId, maxResults):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video=youtube.commentThreads().list(part='snippet, replies', 
                                        videoId=videoId, 
                                        maxResults=maxResults, 
                                        order="relevance", 
                                        textFormat="plainText").execute()
    comments = []
    for item in video['items']:
        comment = item["snippet"]["topLevelComment"]
        name = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        likecount = comment["snippet"]["likeCount"]
        comments.append([text, likecount, name])
    return comments

def postComment(content, videoId):
    CLIENT_FILE = 'client-secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = [
            'https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/youtubepartner'
             ]
    youtube = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
    request_body = {
        'snippet': {
            'videoId': videoId,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': content
                }
            }
        }
    }
    youtube.commentThreads().insert(part='snippet', body=request_body).execute()

def getVideos(keyword, amount):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    videos = youtube.search().list(q=keyword, part="snippet", type="video", maxResults=amount).execute()
    video_list = []
    for item in videos["items"]:
        id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_list.append([id,title])
    return video_list

os.system('cls')
specificVideo = input('DESEJA BUSCAR UM VIDEO ESPECIFICO (Y, N)> ')
if specificVideo.lower() == "y":
    videoId = input('ID DO VIDEO> ')
    specificVideo = True
else:
    videoKeyword = input('PALAVRA CHAVE PARA BUSCAR OS VIDEOS> ')
    videoAmount = input('QUANTIDADE DE VIDEOS QUE DESEJA BUSCAR> ')
    specificVideo = False
specificComment = input('DESEJA COMENTAR ALGO ESPECIFICO (Y, N)> ')
if specificComment.lower() == "y":
    specificComment = input('CONTEUDO DO COMENTARIO> ')
    amountComment = input('QUANTAS VEZES DESEJA COMENTAR> ')
else:
    specificComment = False
    amountComment = input('QUANTOS COMENTARIOS DESEJA CLONAR> ')
inteval = input('INTERVALO PARA EXECUTAR O SCRIPT (MINUTOS)> ')

while True:
    if specificVideo == True:
        if specificComment != False:
            print('\n')
            for i in range(int(amountComment)):
                postComment(specificComment, videoId)
                time.sleep(1)
                print(f"[COMENTANDO] {specificComment[:50]}")
        else:
            print('\n')
            comments = getVideoComments(videoId, amountComment)
            for comment in comments:
                postComment(comment[0], videoId)
                print(f"[COMENTANDO] USER: {comment[2]} | TEXTO: {comment[0][:45]}... | LIKES: {comment[1]}")
    else:
        videos = getVideos(videoKeyword, videoAmount)
        for video in videos:
            print(f"\nVIDEO: {video[1]} | URL: https://www.youtube.com/watch?v={video[0]}\n")
            comments = getVideoComments(video[0], amountComment)
            if specificComment != False:
                for i in range(int(amountComment)):
                    print(video[0])
                    postComment(specificComment, video[0])
                    print(f"[COMENTANDO] {specificComment[:50]}")
                    time.sleep(1)
            else:
                for comment in comments:
                    postComment(comment[0], video[0])
                    print(f"[COMENTANDO] USER: {comment[2]} | TEXTO: {comment[0][:45]}... | LIKES: {comment[1]}")
                    time.sleep(1)

    time.sleep(int(inteval) * 60)



    










