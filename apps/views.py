from django.shortcuts import render
from apps.models import BookmarkWord, SearchedWord
from utils.general_methods import get_json_response


def search_words(request, *args, **kwargs):
    template = 'search_words.html'
    if request.method == 'GET':
        bookmarks = BookmarkWord.objects.filter(user=request.user)
        context_dict = {'bookmarks': bookmarks, 'count': bookmarks.count() if bookmarks else 0}
        return render(request, template, context_dict)

    elif request.method == 'POST':

        if request.is_ajax():
            if request.POST.get('bookmark'):
                word = request.POST.get('word')
                content = {}
                if word:
                    bookmark = BookmarkWord.objects.get_or_create(word=word, user=request.user)
                    content = {"message": "Bookmarked successfully!", "status": "ok"}
                else:
                    content = {"message": "No word specified", "status": "error"}
                return get_json_response(content)

            elif request.POST.get('term'):
                term = request.POST.get('term')
                if term:
                    searched_word = SearchedWord.objects.get_or_create(word=term)
                    content = {"message": "Word saved successfully!", "status": "ok"}
                else:
                    content = {"message": "No word specified", "status": "error"}
                return get_json_response(content)

            elif request.POST.get('delete'):
                bookmark_id = request.POST.get('bookmark_id')
                print "id", bookmark_id
                bookmark = BookmarkWord.objects.filter(pk=int(bookmark_id)).first().delete()
                content = {"message": "Bookmark deleted!"}
                return get_json_response(content)
    else:
        return render(request, template, {"msg": "No request"})