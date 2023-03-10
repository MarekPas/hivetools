from django.shortcuts import render
from beem.comment import Comment, Account
from beem.exceptions import ContentDoesNotExistsException
import random
from .commons import get_int_reputation

BOT_LIST = ('actifit', 'bbhbot', 'beerlover', 'curation-cartel', 'discovery-it', 'ecency', 'germanbot',
            'hivebits', 'hiq.smartbot', 'hive-112281', 'hivebuzz', 'hivegifbot', 'holybread', 'india-leo', 'indiaunited',
            'lolzbot', 'luvshares', 'meme.bot', 'monster-curator', 'pgm-curator', 'pgmcuration', 'pinmapple',
            'pizzabot', 'poshtoken', 'risingstargame', 'splinterboost', 'steem-plus', 'steem-ua', 'steemitboard', 'stemsocial',
            'teamuksupport', 'thepimpdistrict', 'threespeak', 'tipu', 'upvoteturtle', 'wine.bot', 'youarealive', 'zottonetoken')

def comment_picker(request):
    if request.method == "POST":
        try:
            post = Comment(request.POST['post'])
            win_num = int(request.POST.get('winners'))
            min_rep = int(request.POST.get('reputation_min'))
            max_rep = int(request.POST.get('reputation_max'))
        except ContentDoesNotExistsException:
            return render(request, 'picker/picker.html', {'error': 'Post does not exist!'})
        except ValueError:
            return render(request, 'picker/picker.html', {'error': 'Wrong permlink format or reputation is not an integer!'})
        except KeyError:
            return render(request, 'picker/picker.html', {'error': 'Something went wrong! Try again.'})
        except TimeoutError:
            return render(request, 'picker/picker.html', {'error': 'Timeout Error. Please, try again later.'})

        author = post.json().get('author', 'no_author')
        word = request.POST.get('demand')
        bots = request.POST.get('bots')
        followers = request.POST.get('followers')
        exclude_users = tuple(x.strip("@").strip() for x in request.POST.get('exclude_users').split(","))

        replies = post.get_all_replies()

        if bots == "on":
            bot_list = BOT_LIST + (author,) + exclude_users
            replies = [[reply.author, reply.body, get_int_reputation(reply.get('author_reputation'))] for reply in replies if word.lower() in reply.body.lower() and reply.author not in bot_list]
        else:
            excluded = exclude_users + (author,)
            replies = [[reply.author, reply.body, get_int_reputation(reply.get('author_reputation'))] for reply in replies if word.lower() in reply.body.lower() and reply.author not in excluded]

        replies = [r for r in replies if max_rep >= r[2] >= min_rep]   # removing comments with low/high reputation

        if followers == "on":
            f = Account(author).get_followers()
            replies = [reply for reply in replies if reply[0] in f]

        if not replies:
            return render(request, 'picker/picker.html', {'error': 'No valid comments :('})
        
        participants = set(author for author, body, rep in replies)
        
        if win_num <= 1:
            winner = [random.choice(replies)]
            participants.remove(winner[0][0])
            print(post.title, winner)
            return render(request, 'picker/picker.html', {'winners': winner, 'participants': participants, 'post': post})
        elif win_num > len(replies):
            return render(request, 'picker/picker.html', {'error': 'There is more winners than comments. Choose a smaller number of winners.'})
        else:
            winners = random.sample(replies, win_num)
            print(post.title, winners)
            for winner in winners:
                participants.remove(winner[0])
            names = "@" + ", @".join(a for a, b, r in winners)
            return render(request, 'picker/picker.html', {'winners': winners, 'participants': participants, 'post': post, 'names': names})

    else:
        return render(request, 'picker/picker.html', {})


def bots(request):
    return render(request, 'picker/bots.html', {'bots': BOT_LIST})
