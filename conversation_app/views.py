from django.shortcuts import render, get_object_or_404, redirect
from items_app.models import Item
from .forms import ConversationMessageForm
from .models import Conversation
from django.contrib.auth.decorators import login_required


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard_app:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation_app:detail', pk=conversations.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('items_app:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    print(conversations)

    return render(request, 'conversation/inbox.html', {'conversations': conversations})


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    # 印出 user 看是否有資料
    # for i in conversation.messages.all():
    #     print(i.conversation.members.all())

    # print(conversation)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation_app:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {'conversation': conversation, 'form': form})
