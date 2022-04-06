from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from chat import utility_functions as chat_utility_functions
from django.contrib.auth.models import User
from chat.models import Chat, Partecipa, PrivateChat, GroupChannel, Message
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.db.models import Max
from contacts import utility_functions as contacts_utility_functions


@login_required()
def chat_list(request):
    chat_list = chat_utility_functions.get_user_private_chats(request)
    return render(request, 'private-chat-list.html',
                  {'private_chats': chat_list, 'len_chats': len(chat_list)})


@login_required()
def group_list(request):
    group_list = chat_utility_functions.get_user_group_chats(request)
    return render(request, 'group-chat-list.html', {'group_chats': group_list, 'len_chats': len(group_list)})


@login_required()
def new_chat(request):
    addable = chat_utility_functions.get_addable_users_private_chat(request)
    return render(request, 'new-chat.html', {'users': addable, 'len_addable': len(addable)})


@login_required()
def new_group_chat(request):
    addable = chat_utility_functions.get_addable_users_private_chat(request)
    return render(request, 'new-group-chat.html', {'users': addable, 'len_addable': len(addable)})


@login_required
def create_chat(request):
    other_username = request.POST.get("other_username")
    other_user = User.objects.get(username=other_username)
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})


def create_group(request):
    user_list = request.POST.getlist('participants')
    channel_name = request.POST.get("chat_name_input")

    if len(channel_name) == 0:
        channel_name = "Default name"

    group_channel = GroupChannel()
    new_chat = GroupChannel.add_this(group_channel, channel_name)
    create_partecipa(request, new_chat, user_list)
    return group_chat(request, new_chat)  # redirect alla pagina della chat di gruppo


@login_required
def create_partecipa(request, chat, participants_list):
    Partecipa.add_this(Partecipa(), chat, request.user)

    for user in participants_list:
        Partecipa.add_this(Partecipa(), chat, (User.objects.all().get(username=user)))
    return


@login_required
def private_chat(request):
    chat_id = request.POST.get("id_chat")
    chat = PrivateChat.objects.get(id_chat=chat_id)
    messages = Message.objects.all().filter(chat=chat)
    if chat.participant1 == request.user:
        participant = chat.participant2
    else:
        participant = chat.participant1
    return render(request, 'chat.html', {'user2': participant, 'id_chat': chat_id, 'messages': messages})


@login_required
def goto_groupchat_from_id(request):
    chat_id = request.POST.get("id_chat")
    chat = GroupChannel.objects.get(id_chat=chat_id)
    return group_chat(request, chat)


@login_required
def group_chat(request, chat):
    messages = Message.objects.all().filter(chat=chat)
    partecipants = chat_utility_functions.get_group_chat_partecipants(request, chat.id_chat)
    return render(request, 'group-chat.html', {'group_chat': chat, 'messages': messages, 'partecipants': partecipants})


@login_required
def send_message(request):
    chat_id = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=chat_id)
    text_message = request.POST.get("text-message-input")
    if len(text_message) > 0:
        messaggio = Message.add_this(Message(), chat, request.user, text_message)
    response = HttpResponse("200")
    return response


@login_required
def get_message_by_id(id):
    return Message.objects.all().get(id=id)


@login_required
def add_partecipants(request):
    chat_id = request.POST.get("id_chat")
    group = GroupChannel.objects.get(id_chat=chat_id)
    partecipanti = chat_utility_functions.get_addable_user_group_chat(request, chat_id)
    return render(request, 'add_users_group_chat.html', {'users': partecipanti, 'len_addable': len(partecipanti),
                                                         'group': group})


def add_users_to_group(request):
    user_list = request.POST.getlist('participants')
    group_id = request.POST.get("group_id")
    group = GroupChannel.objects.get(id_chat=group_id)
    create_partecipa(request, group, user_list)
    return group_chat(request, group)  # redirect alla chat di gruppo


def get_json_chat_messages(request):
    id_chat = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=id_chat)
    messaggi_query = Message.objects.all().filter(chat=chat)
    messaggi_json_array = []
    for messaggio in messaggi_query:
        msg = {'username': messaggio.sender.username, 'text': messaggio.text,
               'timestamp': messaggio.timestamp.strftime('%Y-%m-%d %H:%M')}
        messaggi_json_array.append(msg)
    return JsonResponse(messaggi_json_array, safe=False)
