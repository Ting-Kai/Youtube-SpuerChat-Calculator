import requests
import re
from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader

def get_comments(video_url):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(video_url)
    return comments

def get_exchange_rates():
    r = requests.get('https://tw.rter.info/capi.php')
    return r.json()

def extract_currency_and_amount(paid_string):
    paid_string = paid_string.strip()
    
    match = re.match(r'([A-Z$¥]+)\s*([\d,]+(?:\.\d+)?)', paid_string)
    
    if match:
        currency = match.group(1)
        amount_str = match.group(2).replace(',', '')
        if currency == '¥':
            currency = 'JPY'
        if currency == '$':
            currency = 'TWD'
        currency = currency.replace('$', 'D')
        amount = float(amount_str)
        
        return currency, amount
    else:
        raise ValueError("Format error, should be in the form of 'Currency$Amount' or 'Amount'.")

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
                currency, amount  = extract_currency_and_amount(comment['paid'])
                
                amount_twd = convert_to_twd(amount, currency, rates)
                total_paid_twd += amount_twd
                
                print(f'amount:{int(amount):<10}amount_twd:{int(amount_twd):<10}currency:{currency:<5}total:{int(total_paid_twd):<10}')

            except ValueError:
                print(f"Cannot parse amount: {comment['paid']}")

    return donation_comments, total_paid_twd

if __name__ == "__main__":

    video_url = input("Please enter the YouTube video URL: ")

    comments = get_comments(video_url)
    rates = get_exchange_rates()
    donation_comments, total_paid_twd = filter_donation_comments(comments, rates)

    print(f"There are {len(donation_comments)} SuperChat comments:")
    print(f"Total Donate Amount: {total_paid_twd}")