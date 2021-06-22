from django.shortcuts import render
import beem
from beem.comment import Comment
import random


def comment_picker(request):
    if request.method == "POST":
        try:
            post = Comment(request.POST['post'])
        except beem.exceptions.ContentDoesNotExistsException:
            return render(request, 'picker.html', {'error': 'Post does not exist!'})
        except ValueError:
            return render(request, 'picker.html', {'error': 'Wrong permlink format!'})
        word = request.POST.get('demand')
        replies = post.get_all_replies()
        replies = [[reply.author, reply.body] for reply in replies if word.lower() in reply.body.lower()]
        if not replies:
            return render(request, 'picker.html', {'error': 'No valid comments :('})
        winner = random.choice(replies)
        print(winner)
        participants = [author for author, body in replies]
        participants.remove(winner[0])

        return render(request, 'picker.html', {'winner': winner, 'participants': participants, 'post': post})
    else:
        return render(request, 'picker.html', {})
