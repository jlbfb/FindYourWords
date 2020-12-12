import logging, os, pickle, re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import WordsForm, WordCollectionForm, WordForm
from .models import Word, WordCollection
from .ws import (grid_builder,
                grid_filler,
                grid_map_export_excel,
                grid_map_export_txt,
                grid_map_display,
                grid_map_for_template,
                diff_and_dir,
                word_placer,
                word_collector,
                save_grid_maps,
                save_collections,
                load_collections)


# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Create your views here.
def index(request, update=''):
    word_list = ''
    difficulty = ''
        
    if request.method == 'POST':
        word_collection_form = WordCollectionForm(data=request.POST)
        words_form = WordsForm(data=request.POST)
        # word_form = WordForm()

        if word_collection_form.is_valid() and words_form.is_valid():
            difficulty = int(request.POST['difficulty']) - 1 
            # print(f'These are the details: {details}')
            request.session['difficulty'] = difficulty
            # request.session['grid_size'] = details['grid_size']
            wc = word_collection_form.cleaned_data['word_collection']
            # wc = re.sub(r'([^a-zA-Z0-9 ]+)','',wc)
            print(f'WC = {wc}')
            request.session['wc'] = wc
            # word_form = word_form.save(commit=False)
            words = words_form.cleaned_data
            print(f'Cleaned words = {words}')
            words_sub = re.sub(r'([^a-zA-Z]+)',' ',words['words'])
            raw_word_list = words_sub.split(' ')
            print(f'Raw Word_list = {raw_word_list}')
            word_list = set()
            for search_word in raw_word_list:
                if not search_word: continue # Filter blanks
                word_list.add(search_word.upper())
            word_list = sorted(list(word_list))
            print(f'Cleaned Word List = {word_list}')
            request.session['word_list'] = word_list
            return HttpResponseRedirect('verify')

        else:
            print(words_form.errors)  # word_collection_form.errors, 

    else:
        path = request.path
        print(f'This is the path: {path}')
        if 'update' in path:
            current_words = request.session['word_list']
            wc = request.session['wc']
            difficulty = request.session['difficulty'] + 1
            for word in current_words:
                word_list = word_list + f'{word}\n'
            print(f'This is the word list: {word_list}')
            words_form = WordsForm(initial={'words':word_list})
            word_collection_form = WordCollectionForm(initial={'word_collection': wc})
        else:
            words_form = WordsForm()
            word_collection_form = WordCollectionForm()
    context = {
        'title': 'Find Your Words',
        'word_collection_form': word_collection_form,
        'words_form': words_form,
        'word_list': word_list,
        'difficulty': difficulty,
    }
    template = 'cws/index.html'
    return render(request, template, context)

def verify(request):

    wc = request.session['wc']
    wc2 = wc.replace(' ','_')
    request.session['wc2'] = wc2
    word_list = request.session['word_list']
    difficulty = request.session['difficulty']

    word_set = word_collector(word_list)
    pickled_word_set = pickle.dumps(word_set).hex()
    request.session['word_set'] = pickled_word_set
    long_word = word_set[0]['word']
    if difficulty < 3:
        if len(long_word) > len(word_set):
            min_grid_size = len(long_word)
        else:
            min_grid_size = len(word_set)
    elif difficulty < 6:
        min_grid_size = len(long_word) + int(len(word_set) * .3)
    else:
        min_grid_size = len(long_word) + int(len(word_set) * .6)

    if request.method == 'POST':
        # details = request.POST
        # print(f'The details: {details}')
        grid_size = request.POST['grid_size']
        print(f'Grid Size = {grid_size} and Integer: {int(grid_size)}')
        request.session['grid_size'] = int(grid_size)
        return HttpResponseRedirect('grid')

    context = {
        'title': 'Verify Your Words',
        'wc': wc,
        'word_list': word_list,
        'difficulty': difficulty,
        'min_grid_size': min_grid_size,
    }
    try:
        build_fail = request.session['build_fail']
        context['build_fail'] = build_fail
        request.session['build_fail'] = 0
    except:
        pass
    template = 'cws/verify.html'
    return render(request, template, context)

def grid(request):

    difficulty = request.session['difficulty']
    grid_size = request.session['grid_size']
    pickled_word_set = request.session['word_set']
    word_set = pickle.loads(bytes.fromhex(pickled_word_set))
    # word_set = word_collector(word_list)
    word_set = diff_and_dir(difficulty, word_set)
    grid_map = grid_builder(grid_size)
    # logger.info(f'Grid Map starts as: {grid_map}')
    grid_map = word_placer(word_set, grid_size, grid_map, difficulty)
    if grid_map == 'CannotBuild':
        word_list = request.session['word_list']
        logger.info(f'Could not build (Grid: {grid_size}, '
            f'Diff: {difficulty}): {word_list}')
        request.session['build_fail'] = 1
        return HttpResponseRedirect('verify')    
    # Print grid map
    grid_map_display(grid_size, grid_map)
    grid_map = grid_filler(word_set, grid_size, difficulty, grid_map)
    # Print grid map
    grid_map_display(grid_size, grid_map)
    request.session['grid_map'] = grid_map
    logger.info(f'The grid map has been created')
    return HttpResponseRedirect('board')

def board(request):

    wc = request.session['wc']
    wc2 = request.session['wc2']
    word_list = request.session['word_list']
    grid_size = request.session['grid_size']
    grid_map = request.session['grid_map']

    if request.method == 'POST':
        options = request.POST['submit']
        print(f'Options: {options}')
        if 'Save' in options:
            word_collection = WordCollection.objects.create(word_collection=wc)
            # wc_id = WordCollection.objects.get(pk=word_collection.pk)
            print(f'Word Collection: {word_collection}-{word_collection.pk}')
            for search_word in word_list:
                Word.objects.create(word_collections = word_collection, word = search_word)
                print(f'Saved: {search_word}')
        elif 'Text Grid' in options:
            grid_map_export_txt(grid_size, grid_map, wc, wc2, word_list)
            request.session['file_name'] = f'{wc2}.txt'
        elif 'Text Key' in options:
            grid_map_export_txt(grid_size, grid_map, wc, wc2, word_list, key='Y')
            request.session['file_name'] = f'{wc2}_Key.txt'
        elif 'Excel Grid' in options:
            grid_map_export_excel(grid_size, grid_map, wc, wc2, word_list)
            request.session['file_name'] = f'{wc2}.xlsx'
        elif 'Excel Key' in options:
            grid_map_export_excel(grid_size, grid_map, wc, wc2, word_list, key='Y')
            request.session['file_name'] = f'{wc2}_Key.xlsx'

        return HttpResponseRedirect('download')

    else:
        grid_map_template = grid_map_for_template(grid_size, grid_map)
        request.session['grid_map_template'] = grid_map_template
    
    context = {
        'title': 'Find Your Words',
        'wc': wc,
        'word_list': word_list,
        'grid_map_template': grid_map_template
    }
    template = 'cws/board.html'
    return render(request, template, context)

def print_view(request):
    grid_map_template = request.session['grid_map_template']
    wc = request.session['wc']
    word_list = request.session['word_list']
    grid_size = request.session['grid_size']

    context = {
        'title': 'Print Your Words',
        'wc': wc,
        'word_list': word_list,
        'grid_size': grid_size,
        'grid_map_template': grid_map_template
    }
    template = 'cws/print_view.html'
    return render(request, template, context)

def download(request):
    file_name = request.session['file_name']
    context = {
        'title': 'Download Your Board',
        'file_name': file_name
    }
    template = 'cws/download.html'
    return render(request, template, context)

def delete_board(request):
    file_name = request.session['file_name']
    os.remove(f'./media/grids/{file_name}')

    return HttpResponseRedirect('board')