import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import UserProfile
# ,Message,UserRoom
from movies.models import Movie, Clue
# from movies.forms import MovieForm, ClueForm, ClueFilterForm


class GuessGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_id = self.scope["url_route"]["kwargs"]["session_code"]
        self.room_id =123456
        print(self.scope)
        if self.scope["user"].is_anonymous:
            print(self.room_id)
            await self.close()
        else:
            print(self.room_id)
            # Use a common chat room for everyone
            self.room_group_name = 'global_gamechat_room'  # Fixed room name

            self.clues = await self.get_all_clue()
            
            print(' self.clues : ')
            print(self.clues)
            self.inverted_dictionary=dict()
            for c in self.clues:
                print(f"c : {c}")
                
                # if c.movie.title in ['DDLJ']:
                if c["movie"] not in self.inverted_dictionary:
                    self.inverted_dictionary[c["movie"]]=[c]
                    for i in self.inverted_dictionary[c["movie"]]:
                        if i['clue_type']==c['clue_type']:
                            print(f"i : {i}")                            
                            i=c
                            break;  

                else:
                    self.inverted_dictionary[c["movie"]].append(c)

            print(self.inverted_dictionary)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name

            )
            await self.accept()

            # # Send room name and chat history to the connected user
            # await self.send(text_data=json.dumps({
            #     'inverted_dictionary': self.inverted_dictionary,
            # }))
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_clues',
                'inverted_dictionary': self.inverted_dictionary,
                # 'chat_history': self.chat_history
            }
        )
            

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
       )

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.clueId = data['clue_id']
        self.sessionCode = data['session_code']
        self.movie_exp=data['movie_exp']
        self.guess = data['guess']
        self.timestamp = data['timestamp']
        self.result='Incorrect'
        sent_by_user = data.get('sent_by_user', self.scope["user"].id)
        # sent_to_user = data.get('sent_to_user', None)  # Optional for group

        if not self.guess:
            print('Error:: empty guess')
            return

        
        # Broadcast to everyone in the room
        
        self.guess=self.guess.lower().strip()
        self.movie_exp=self.movie_exp.lower().strip()
        if self.guess==self.movie_exp:
            self.result='correct'
            self.guess=''
        data= {
                'timestamp': self.timestamp,
                'result':self.result,
                'user':sent_by_user,
                'clueId':self.clueId
            }
        print(data)

        await self.channel_layer.group_send(
            self.room_group_name,
           
             {
                'type': 'receive_group_message',
                'timestamp': self.timestamp,
                'result':self.result,
                'guess':self.guess,
                'user':sent_by_user,
                'clueId':self.clueId
                
            }
            
        )

    async def receive_group_message(self, event):
        # Send to WebSocket (no need manual double send!)
        await self.send(text_data=json.dumps(
            {"get_updates":
             [{
                'timestamp': event['timestamp'],
                'result': event['result'],
                'user': event['user'],
                'guess': event['guess'],
                'clueId': event['clueId']
            }]
            }))

    async def send_clues(self, event):
        # Send to WebSocket (no need manual double send!)
        await self.send(text_data=json.dumps(
            {'get_questions':[event['inverted_dictionary']]}
        ))

    @database_sync_to_async
    def get_all_clue(self):
        clues = Clue.objects.select_related('movie').all()

        return [
            {
                'clue_type': clue.clue_type,
                'movie': clue.movie.title,
                'content': clue.content,
                
            }
            for clue in clues
        ]

    # @database_sync_to_async
    # def get_chat_history(self):
    #     return list(Message.objects.values('sender', 'receiver', 'content'))
    
        # messages = Message.objects.select_related('sender', 'receiver').all()

        # return [
        #     {
        #         'sender': msg.sender.members,
        #         'receiver': msg.receiver.members,
        #         'content': msg.content,
        #         'timestamp': msg.timestamp.isoformat()
        #     }
        #     for msg in messages
        # ]
    # @database_sync_to_async
    # def get_user_object(self, user_id):
    #     try:
    #         return User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         return None

    # @database_sync_to_async
    # def create_message(self, sender, receiver_id, content):
    #     receiver = None
    #     if receiver_id:
    #         try:
    #             receiver = User.objects.get(id=receiver_id)
    #         except User.DoesNotExist:
    #             pass
    #     else:
    #         receiver = UserRoom.objects.all()
    #         msg_arr=[]
    #         for i in receiver:
    #             if sender==i.members:
    #                 continue
    #             print(i.members)
    #             msg=Message.objects.create(sender=sender, receiver=i.members, content=content)
    #             msg_arr.append(msg)
    #         return [{
    #                 'sender': msg.sender.username,
    #                 'receiver': msg.receiver.username,
    #                 'content': msg.content,
    #                 'timestamp': msg.timestamp.isoformat()
    #             } for msg in msg_arr]
    #     msg_arr=[Message.objects.create(sender=sender, receiver=receiver, content=content)]
    #     return [{
    #                 'sender': msg.sender.username,
    #                 'receiver': msg.receiver.username,
    #                 'content': msg.content,
    #                 'timestamp': msg.timestamp.isoformat()
    #             } for msg in msg_arr]

