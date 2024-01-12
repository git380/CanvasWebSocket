import asyncio
import json

import websockets

# クライアントの管理用のセット
clients = set()
# お絵かきデータの保存
canvas_history = []


async def echo(websocket):
    # 接続が確立された
    print('クライアントが接続しました。')
    # 新しいクライアントのWebSocket接続をclientsセットに追加
    clients.add(websocket)
    try:
        # 過去のチャット履歴を送信
        for message in canvas_history:
            await websocket.send(json.dumps(message))

        async for message in websocket:
            print(f'受信内容：{message}')
            # クリアイベントの処理
            if message == 'clear':
                canvas_history.clear()
                # すべての接続されたクライアントにブロードキャスト
                for client in clients:
                    if client != websocket:
                        # 自分以外の全員に送る
                        await client.send(message)
            else:
                data = json.loads(message)
                # お絵かきデータの保存
                canvas_history.append(data)
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
