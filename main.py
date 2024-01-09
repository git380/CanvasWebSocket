import asyncio
import websockets
import json

# クライアントの管理用のセット
clients = set()


async def echo(websocket):
    # 接続が確立された
    print('クライアントが接続しました。')
    # 新しいクライアントのWebSocket接続をclientsセットに追加
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f'受信内容：{message}')
            data = json.loads(message)
            # クリアイベントの処理
            if data.get('type') == 'clear':
                # すべての接続されたクライアントにブロードキャスト
                for client in clients:
                    if client != websocket:
                        # 自分以外の全員に送る
                        await client.send(json.dumps(data))
            else:
                # クライアントからのお絵かきデータをすべてのクライアントにブロードキャスト
                for client in clients:
                    if client != websocket:
                        # 自分以外の全員に送る
                        await client.send(json.dumps(data))
    finally:
        # クライアントが切断された場合、セットから削除
        clients.remove(websocket)
        print('接続が切断されました。')

print('サーバー起動中...')

# イベントループの開始
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8124))
asyncio.get_event_loop().run_forever()
