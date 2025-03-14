import requests
from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader

def get_comments(video_url):

    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(video_url)
    return comments

def get_exchange_rates():
    r = requests.get('https://tw.rter.info/capi.php')
    return r.json()

def convert_to_twd(amount, currency, rates):

    if currency == 'TWD':
        return amount

    if currency == 'USD':
        amount_twd = amount * rates['USDTWD']['Exrate']
    else:
        amount_usd = amount / rates[f'USD{currency}']['Exrate']
        amount_twd = amount_usd * rates['USDTWD']['Exrate']
    
    return amount_twd

def filter_donation_comments(comments, rates):
    donation_comments = []
    total_paid_twd = 0.0
    for comment in comments:
        if 'paid' in comment and comment['paid']:
            donation_comments.append(comment)

            try:
                if len(comment['paid'].split('$')) < 2:
                    
                    print(f"格式錯誤: {comment['paid']}")
                    continue
                
                amount = float(comment['paid'].split('$')[1].replace(',', ''))

                currency = (comment['paid'].split('$')[0].strip() + 'D') if comment['paid'].split('$')[0].strip() else 'TWD'
                
                amount_twd = convert_to_twd(amount, currency, rates)

                total_paid_twd += amount_twd

                print(f'amount: {amount}; amount_twd: {amount_twd}; currency: {currency}; total: {total_paid_twd}')

            except ValueError:

                print(f"無法解析金額: {comment['paid']}")

    return donation_comments, total_paid_twd

if __name__ == "__main__":

    # video_id = input("請輸入 YouTube 影片網址：")
    video_id = "https://www.youtube.com/watch?v=wTdpLsX8iog"

    comments = get_comments(video_id)

    rates = get_exchange_rates()

    donation_comments, total_paid_twd = filter_donation_comments(comments, rates)

    print(f"共有 {len(donation_comments)} 條 SuperChat 留言：")
    print(f"Total  Donate Amount: {total_paid_twd}")

    


