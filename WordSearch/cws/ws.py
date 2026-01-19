import logging, re
# from wordSearchDB import WordSearchDB
from random import randint
from openpyxl import Workbook
from openpyxl.styles import Alignment
from tempfile import NamedTemporaryFile
from .ws_config import directions, diff_dir, diff_fill
from django.conf import settings


# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def timer(fn):
    from time import perf_counter
    def calculate(*args, **kwargs):
        start = perf_counter()
        call_func = fn(*args, **kwargs)
        end = perf_counter()
        elapsed = end - start
        print(f'{fn.__name__} took {elapsed}')
        return call_func
    return calculate

def word_collector(word_list: list):
    """
    Captures the user's word collection
    """
    # global word_collection
    # global word_list
    # word_collection = input('Enter the collection name: ')
    # while True:
    #     if re.match("^[a-zA-Z0-9 ]*$", word_collection):
    #         break
    #     else:
    #         word_collection = input('Enter a valid collection name: ')
    # words = []
    # for i in range(0,int(n)):
    #     next_word = (input(f'Enter word {i}: '))
    #     while True:
    #         if re.match("^[a-zA-Z]*$", next_word):
    #             if next_word.upper() in words:
    #                 next_word = input(f'Duplicate word.  Please enter an '
    #                     f'alternate word {i}: ')
    #             else: break
    #         else:
    #             next_word = input(f'Please enter a valid word {i}: ')
    #     words.append(next_word.upper())
    # word_list = sorted(words)
    # change_word()
    # word_list = sorted(word_list)
    words = sorted(word_list, key = lambda x: len(x))
    words.reverse()
    print(f'Words sorted by length: {words}')
    print(f'Word List: {word_list}')
    word_set = dict()
    # count = 0
    for count in range(0,len(words)):
        word_set[count] = {'word': words[count], 'set': {*words[count]}}
        # count += 1
    print(f'Word Set: {word_set}')
    return word_set

# def change_word():
#     global word_list
#     global changed_words
#     changed_words = []
#     while True:
#         change_word = input('Would you like to change any words (Y/N)? ')
#         if re.match("^[yY]{1,1}$", change_word):
#             for count in range(0, len(word_list)):
#                 print(f'{count}: {word_list[count]}')
#             while True:
#                 word_num = input('Enter the number of the word to change: ')
#                 if re.match("^[0-9]{1,2}$", word_num):
#                     word_num = int(word_num)
#                     try:
#                         print(f'The word to change: {word_list[word_num]}')
#                         changed_words.append(word_num)
#                         while True:
#                             new_word = input('Enter the new word: ')
#                             if re.match("^[a-zA-Z]*$", new_word):
#                                 if new_word.upper() in word_list:
#                                     print('That is a duplicate word.')
#                                     continue
#                                 word_list[word_num] = new_word.upper()
#                                 print('Your word list has been updated.')
#                                 break
#                             else:
#                                 print('That is not a valid word.')
#                     except Exception as e:
#                         print(f'{e}\nThat is not a valid selection.')
#                         continue
#                     break
#                 else:
#                     print('That is not a valid selection.')
#         else:
#             break
#     return

def grid_builder(grid: int):
    """
    Builds the grid map based upon the selected grid size
    """
    # global grid_map
    grid_map = dict()
    for i in range(0,grid):
        for j in range(0,grid):
            grid_map[f'{i}-{j}'] = '.'
    print('Grid built')
    return grid_map

'''
def integer_check(fn: str, num: int):
    """
    Verifies that input is an integer and calls the needed function
    """
    while True:
        try:
            num = int(num)
            break
        except:
            num = input('Please enter a whole number:')
            continue
    return fn(num)
'''

def diff_and_dir(difficulty, word_set):
    """
    Set word direction based upon the chosen difficulty level
    """
    randomizer = str()
    # print(diff_dir)
    for d, p in diff_dir[difficulty]:
        randomizer = randomizer + (str(d) * int(p * 100))
        # print(randomizer)
    for count in range(0,len(word_set)):
        rand_int = randint(0,99)
        # print(rand_int)
        dir_select = randomizer[rand_int]
        word_set[count]['dir'] = directions[int(dir_select)]
        # print(rand_int, dir_select, word_set[count]['dir'])
    return word_set

@timer
def word_placer(word_set, grid, grid_map, difficulty):
    """
    Determine the position of the search words within the grid
    """
    count = 0
    total_conflicts = 0
    while count < len(word_set):
        print(f'Count = {count}')
        conflict = 0
        while True:
            cross = 0
            if conflict >= 20:
                # logger.info(f'Crossing word conflict: {conflict}')
                total_conflicts += 1
                if total_conflicts >= 50:
                    return 'CannotBuild'
                if total_conflicts % 5 == 0:
                    logger.info(f'Total Conflicts: {total_conflicts}')
                    # total_conflicts = 0
                    word_set = diff_and_dir(difficulty, word_set)
                grid_map = grid_builder(grid)
                count = 0
                break
            this_word = word_set[count]['word']
            word_len = len(word_set[count]['word'])
            x_dir = word_set[count]['dir'][1]
            y_dir = word_set[count]['dir'][2]
            if x_dir > 0:
                start_x = randint(0, grid - word_len) # - 1)
            elif x_dir < 0:
                start_x = randint(word_len - 1, grid - 1)
            else:
                start_x = randint(0, grid - 1)
            if y_dir > 0:
                start_y = randint(0, grid - word_len) # - 1)
            elif y_dir < 0:
                start_y = randint(word_len - 1, grid-1)
            else:
                start_y = randint(0, grid - 1)
            # print(f'Grid: {grid}')
            # print(f'Grid Map:  {grid_map}')
            print(f'start_x:{start_x}, start_y:{start_y}, x_dir:{x_dir},'
                f'y_dir:{y_dir}, word_len:{word_len}, grid:{grid}')
            print(f'x ending space: {start_x + (x_dir * (word_len - 1))}')
            print(f'y ending space: {start_y + (y_dir * (word_len - 1))}')
            if 0 <= (start_x + (x_dir * (word_len - 1))) < grid:
                if 0 <= (start_y + (y_dir * (word_len - 1))) < grid:
                    print(f"{this_word} starting space is {start_x},{start_y}")
                    letters = dict()
                    letters[0] = grid_map[f'{start_x}-{start_y}']
                    for char in range(1, word_len):
                        letters[char] = grid_map[f'{start_x + (x_dir * char)}'
                            f'-{start_y + (y_dir * char)}']
                    for char in range(0, word_len):
                        if (letters[char] != '.'
                                and letters[char] != this_word[char]):
                            cross = 1
                            conflict += 1
                            print(f'Crossing word conflict: {conflict}')
                            break
                    if cross == 0:
                        grid_map[f'{start_x}-{start_y}'] = this_word[0], 1
                        for char in range(1, word_len):
                            grid_map[f'{start_x + (x_dir * char)}-'
                                f'{start_y + (y_dir * char)}'
                                ] = this_word[char], 1
                        count += 1
                        break
                else:
                    print(f"{word_set[count]['word']}"
                        f" does not fit from y{start_y}")
            else:
                print(f"{word_set[count]['word']}"
                    f" does not fit from x{start_x}")
    return grid_map

@timer
def grid_filler(word_set, grid, difficulty, grid_map):
    word_chars = str()
    for count in range(0,len(word_set)):
        word_chars = word_chars + str(word_set[count]['word'])
    for i in range(0, grid):
        for j in range(0, grid):
            # global grid_map
            char_picker = randint(0,99)
            char_picker = ('alpha' if char_picker < diff_fill[difficulty][0]
                else 'words')
            # print(char_picker, word_chars)
            rand_char = (randint(0,len(word_chars)-1) if char_picker == 'words'
                else randint(65,90))
            # print(rand_char)
            rand_char = (chr(rand_char) if char_picker == 'alpha'
                else word_chars[rand_char].upper())
            try:
                if grid_map[f'{i}-{j}'][1] == 1:
                    continue
            except:
                grid_map[f'{i}-{j}'] = (rand_char, 0)
    return grid_map

def grid_map_display(grid, grid_map):
    for i in range(0,grid):
        print()
        for j in range(0,grid):
            print(grid_map[f'{i}-{j}'][0], end = '')
    print()

def grid_map_for_template(grid, grid_map):
    grid_map_template = []
    grid_map_template.append('<table><tbody>')
    for i in range(0,grid):
        grid_map_template.append('<tr>')
        for j in range(0,grid):
            grid_map_template.append(f'<td class="grid">{grid_map[f"{i}-{j}"][0]}</td>')
        grid_map_template.append('</tr>')
    grid_map_template.append('</tbody></table>')
    return grid_map_template

@timer
def grid_map_export_txt(grid, grid_map, word_collection, wc2, word_list, key = 'N'):
    if key == 'Y':
        text_file = f'{settings.MEDIA_ROOT}/grids/{wc2}_Key.txt'
    else:
        text_file = f'{settings.MEDIA_ROOT}/grids/{wc2}.txt'
    with open(text_file, 'w') as f:
        f.write(f'Word Search\n{word_collection}\n\n')
        for i in range(0,grid):
            f.write('\n')
            for j in range(0,grid):
                if grid_map[f'{i}-{j}'][1] == 1:
                    f.write(grid_map[f'{i}-{j}'][0])
                else:
                    if key == 'Y':
                        f.write('.')
                    else:
                        f.write(grid_map[f'{i}-{j}'][0])
                f.write(' ')
        f.write('\n\n')
        for word in word_list:
            f.write(f"{word}\n")
    print('Done')

@timer
def grid_map_export_excel(grid, grid_map, word_collection, wc2, word_list, key = 'N'):
    cell_ctr = Alignment(horizontal='center')
    wb = Workbook()
    ws = wb.active
    ws.title = word_collection
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=grid)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=grid)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=grid)
    ws.cell(row = 1, column = 1).value = 'Word Search'
    ws.cell(row = 1, column = 1).alignment = cell_ctr
    ws.cell(row = 2, column = 1).value = word_collection
    ws.cell(row = 2, column = 1).alignment = cell_ctr
    curr_row = 3
    for i in range(0,grid):
        curr_col = 1
        curr_row += 1
        for j in range(0,grid):
            ws.column_dimensions[chr(curr_col + 64)].width = 2.5
            if grid_map[f'{i}-{j}'][1] == 1:
                ws.cell(row = curr_row, column = curr_col
                    ).value = grid_map[f'{i}-{j}'][0]
            else:
                if key == 'Y':
                    ws.cell(row = curr_row, column = curr_col).value = '.'
                else:
                    ws.cell(row = curr_row, column = curr_col
                        ).value = grid_map[f'{i}-{j}'][0]
            ws.cell(row = curr_row, column = curr_col
                ).alignment = cell_ctr
            curr_col += 1
    curr_row += 1
    ws.merge_cells(start_row=curr_row, start_column=1,
        end_row=curr_row, end_column=grid)
    for word in word_list:
        curr_row += 1
        ws.cell(row = curr_row, column = 1
            ).value = word
    # TODO: Add Try/ Except handling to cover file being open with same name
    if key == 'Y':
        # with NamedTemporaryFile() as tmp:
        #     wb.save(tmp.name)
        #     tmp.seek(0)
        #     stream = tmp.read()
        wb.save(f'{settings.MEDIA_ROOT}/grids/{wc2}_Key.xlsx')
    else:
        wb.save(f'{settings.MEDIA_ROOT}/grids/{wc2}.xlsx')
    print('Done')

@timer
def save_collections():
    global this_key
    global word_collection
    while True:
        try:
            tw.insert_table('Word_Collections',
                word_collection = (word_collection,))
            this_key = tw.get_key('Word_Collections', id_ = 'id',
                identifier = 'word_collection', value = word_collection)[0]
            for w in range(0, len(word_set)):
                if w == len(word_set) - 1:
                    loop = 'last'
                else:
                    loop = 'next'
                tw.insert_table('Words', word_collections_id = this_key,
                    word = word_set[w]['word'], loop = loop)
            break
        except Exception as e:
            print(e)
            word_collection = input('Please enter another name for the '
                'collection: ')

@timer
def save_grid_maps():
    this_grid = tw.get_key('Grid_Maps', id_ = 'grid_maps_id')
    if this_grid == []:
        this_grid = 1
    else:
        this_grid = max(this_grid)
        print(this_grid)
        this_grid = this_grid[0] + 1
    print(this_grid)
    for i in range(0, grid):
        for j in range(0, grid):
            if j == grid - 1:
                loop = 'last'
            else:
                loop = 'next'
            tw.insert_table('Grid_Maps', loop = loop, grid_maps_id = this_grid,
                cell = f'{i}-{j}', letter = grid_map[f'{i}-{j}'][0],
                word_key = grid_map[f'{i}-{j}'][1])
    tw.insert_table('Collection_Grid', word_collections_id = this_key,
        grid_maps_id = this_grid, difficulty = difficulty, grid_size = grid)

def load_collections():
    global word_list
    word_list = []
    collection_list = tw.get_data('Word_Collections', columns = '*')
    print('Available collections:')
    for collection in collection_list:
        print(f'{collection[0]}: {collection[1]}')
    while True:
        collection = input('Select the list to load: ')
        if re.match('^[0-9]{1,2}$', collection):
            try:
                collection = int(collection)
                words = tw.get_data('Words', columns = '*',
                    condition = f"word_collections_id = \'{collection}\'")
                print(f'Words in the {collection_list[collection - 1][1]} '
                    'Collection:')
                for word in words:
                    word_list.append(word[2])
                    print(word[2])
                break
            except Exception as e:
                print(f'{e}\nThat is not a valid selection.')
        else:
            print('That is not a valid selection.')
    change_word()
    if changed_words != []:
        for change in changed_words:
            # print(f'change = {change}, collection = {collection_list[collection - 1][1]},'
            #     f' new word = {word_list[change]}')
            tw.update_data('Words', word = word_list[change],
                id = words[change][0])
            print(f'Replaced {words[change][0]} with {word_list[change]}')
    else:
        print('No changes made.')


# Start of script
'''
# Variables
cell_ctr = Alignment(horizontal='center')
# tw = WordSearchDB('WordSearch.db')

# TODO:  Set a minimum of 2 words
num_words = input('Enter the number of words in collection: ')
word_set = integer_check(word_collector, num_words)

long_word = word_set[0]['word']
min_grid_size = len(long_word) + int(len(word_set) * .5)

grid = input(f'Enter the grid size (minimum {min_grid_size}): ')
while True:
    if not re.match("^[0-9]{1,2}$", grid) or int(grid) < min_grid_size:
        grid = input(f'Please enter a number between {min_grid_size}-99: ')
        continue
    grid = int(grid)
    break

grid_map = integer_check(grid_builder, grid)

difficulty = input('Please enter the difficulty level (0-9): ')
while True:
    if not re.match("^[0-9]{1,1}$", difficulty):
        difficulty = input('Please enter a number between 0-9: ')
        continue
    difficulty = int(difficulty)
    break

diff_and_dir()

word_placer()

grid_map_display()

grid_filler()

grid_map_display()

export = input(f'Export {word_collection} Word Search to text file (Y/N)? ')
if re.match('^[yY]{1,1}$', export):
    grid_map_export_txt()

export_key = input(f'Export Key for {word_collection} Word Search to text '
    f'file (Y/N)? ')
if re.match('^[yY]{1,1}$', export):
    grid_map_export_txt(key = 'Y')

export = input(f'Export {word_collection} Word Search to Excel file (Y/N)? ')
if re.match('^[yY]{1,1}$', export):
    grid_map_export_excel()

export_key = input(f'Export Key for {word_collection} Word Search to Excel '
    f'file (Y/N)? ')
if re.match('^[yY]{1,1}$', export_key):
    grid_map_export_excel(key = 'Y')

save_collection = input(f'Save {word_collection} Word Collection to database '
    '(Y/N)? ')
if re.match('^[yY]{1,1}$', save_collection):
    save_collections()
    save_grid_map = input(f'Save {word_collection} Word Search puzzle to '
        'database (Y/N)? ')
    if re.match('^[yY]{1,1}$', save_grid_map):
        save_grid_maps()

load_collection = input('Would you like to load an existing Word Collection '
    '(Y/N)? ')
if re.match('^[yY]{1,1}$', load_collection):
    load_collections()


# change_word = input(f'Change any words in {word_collection} (Y/N)?')
# TODO:  Add functionality to pull down the words and go through them one
# at a time and allow for changes; have the word replaced in the db.
'''