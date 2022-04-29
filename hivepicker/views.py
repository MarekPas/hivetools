from django.shortcuts import render
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException
import random


def comment_picker(request):
    if request.method == "POST":
        try:
            post = Comment(request.POST['post'])
            win_num = int(request.POST.get('winners'))
        except ContentDoesNotExistsException:
            return render(request, 'picker/picker.html', {'error': 'Post does not exist!'})
        except ValueError:
            return render(request, 'picker/picker.html', {'error': 'Wrong permlink format!'})
        except TypeError:
            return render(request, 'picker/picker.html', {'error': 'Number of winners is not an integer!'})
        except KeyError:
            return render(request, 'picker/picker.html', {'error': 'Something went wrong! Try again.'})
        except TimeoutError:
            return render(request, 'picker/picker.html', {'error': 'Timeout Error. Please, try again later.'})

        author = post.json().get('author', 'no_author')
        word = request.POST.get('demand')
        bots = request.POST.get('bots')
        replies = post.get_all_replies()

        if bots == "on":
            bot_list = ['actifit', 'beerlover', 'curation-cartel', 'discovery-it', 'ecency', 'gangstalking', 'germanbot', 'hivebits', 'hivebuzz',
                        'hivegifbot', 'holybread', 'india-leo', 'lolzbot', 'luvshares', 'pgm-curator', 'pinmapple',
                        'pizzabot', 'poshtoken', 'risingstargame', 'steem-plus', 'steem-ua', 'steemitboard', 'teamuksupport', 'threespeak', 'tipu',
                        'upvoteturtle', 'voinvote2', 'voinvote3', 'wine.bot', 'youarealive', 'zottonetoken']
            bot_list.append(author)
            replies = [[reply.author, reply.body] for reply in replies if word.lower() in reply.body.lower() and reply.author not in bot_list]
        else:
            replies = [[reply.author, reply.body] for reply in replies if word.lower() in reply.body.lower() and reply.author != author]
        
        if not replies:
            return render(request, 'picker/picker.html', {'error': 'No valid comments :('})
        
        participants = set(author for author, body in replies)
        
        if win_num == 1:
            winner = [random.choice(replies)]
            participants.remove(winner[0][0])
            print(winner)
            return render(request, 'picker/picker.html', {'winners': winner, 'participants': participants, 'post': post})
        elif win_num > len(replies):
            return render(request, 'picker/picker.html', {'error': 'There is more winners than comments. Choose a smaller number of winners.'})
        else:
            winners = random.sample(replies, win_num)
            print(winners)
            for winner in winners:
                participants.remove(winner[0])
            return render(request, 'picker/picker.html', {'winners': winners, 'participants': participants, 'post': post})

    else:
        return render(request, 'picker/picker.html', {})


def splinterlands(request):
    pass
