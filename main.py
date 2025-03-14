from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader

def get_comments(video_url):

    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(video_url)
    return comments

def filter_donation_comments(comments):
    donation_comments = []
    for comment in comments:
        if 'paid' in comment and comment['paid']:
            donation_comments.append(comment)
            print(f"comment: {comment['text']} ; paid: {comment['paid']}")
    return donation_comments

if __name__ == "__main__":

    video_id = input("請輸入 YouTube 影片網址：")

    comments = get_comments(video_id)

    donation_comments = filter_donation_comments(comments)

    print(f"共有 {len(donation_comments)} 條 SuperChat 留言：")
