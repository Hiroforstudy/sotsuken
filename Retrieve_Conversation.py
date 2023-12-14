import requests

access_token = '***' # ここにアクセストークン
owner = '***' # #レポジトリのオーナー名
repo = '***' # レポジトリ名

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# クローズド状態のプルリクエストを取得
url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed'

response = requests.get(url, headers=headers)
if response.status_code == 200:
    pull_requests = response.json()

    # 全てのプルリクエストの情報を取得するためにページネーションを行う
    while 'next' in response.links:
        next_url = response.links['next']['url']
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            pull_requests += response.json()
        else:
            print(f'プルリクエストの取得に失敗しました。')
            break

    # 各プルリクエストの情報を処理する
    for pull_request in reversed(pull_requests):
        pull_number = pull_request['number']
        issue_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}'
        issue_response = requests.get(issue_url, headers=headers)

        if issue_response.status_code == 200:
            issue = issue_response.json()
            issue_comments_url = issue['comments_url']

            issue_comments_response = requests.get(issue_comments_url, headers=headers)
            if issue_comments_response.status_code == 200:
                issue_comments = issue_comments_response.json()
                for issue_comment in issue_comments:
                    comment_message = issue_comment['body'].strip()
                    if comment_message != "":
                        print(comment_message)
            else:
                print(f'プルリクエスト {pull_number} のissue関連のコメント情報の取得に失敗しました。')

        reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'
        comments_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'

        reviews_response = requests.get(reviews_url, headers=headers)
        comments_response = requests.get(comments_url, headers=headers)

        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
            for review in reviews:
                comment_message = review['body'].strip()
                if comment_message != "":
                    print(comment_message)
        else:
            print(f'プルリクエスト {pull_number} のレビュー情報の取得に失敗しました。')

        if comments_response.status_code == 200:
            comments = comments_response.json()
            for comment in comments:
                comment_message = comment['body'].strip()
                if comment_message != "":
                    print(comment_message)
        else:
            print(f'プルリクエスト {pull_number} のコメント情報の取得に失敗しました。')

else:
    print('プルリクエストの取得に失敗しました。')