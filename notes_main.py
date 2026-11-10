from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

# notes = {
#     'Welcome!' :{
#         "text" : "this is the best note taking app in the world!",
#         "tags" : ["good", "instructions"]
#     }
# }
# with open('notes_data.json', 'w')as file:
#     json.dump(notes,file,ensure_ascii=False)

app = QApplication([])
window = QWidget()
window.setWindowTitle('Smart notes')
window.resize(900,600)

field_text = QTextEdit()

lb_list_notes = QLabel('List of notes')
list_notes = QListWidget()
btn_note_create = QPushButton('Create note')
btn_note_delete = QPushButton('Delete note')
btn_note_save = QPushButton('Save note')

lb_list_tags = QLabel('List of tags')
list_tags = QListWidget()
btn_tag_add = QPushButton('Add to note')
btn_tag_untag = QPushButton('Untag from note')
btn_tag_search = QPushButton('Search notes by tag')
search_tag = QLineEdit()
search_tag.setPlaceholderText('Enter tag...')

col_left = QVBoxLayout()
col_left.addWidget(field_text)

col_right = QVBoxLayout()
col_right.addWidget(lb_list_notes)
col_right.addWidget(list_notes)
layout_btn_1 = QHBoxLayout()
layout_btn_1.addWidget(btn_note_create)
layout_btn_1.addWidget(btn_note_delete)

col_right.addLayout(layout_btn_1)
col_right.addWidget(btn_note_save)

col_right.addWidget(lb_list_tags)
col_right.addWidget(list_tags)
col_right.addWidget(search_tag)
layout_btn_2 = QHBoxLayout()
layout_btn_2.addWidget(btn_tag_add)
layout_btn_2.addWidget(btn_tag_untag)

col_right.addLayout(layout_btn_2)
col_right.addWidget(btn_tag_search)

main_layout = QHBoxLayout()
main_layout.addLayout(col_left,stretch=2)
main_layout.addLayout(col_right,stretch=1)
window.setLayout(main_layout)

def add_note():
    note_name,ok = QInputDialog.getText(window,'add note','note name:')
    if ok and note_name != '':
        notes[note_name] = {'text': '','tags':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['tags'])
        print(notes)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['text'] = field_text.toPlainText()
        with open('notes_data.json', 'w')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print('Tidak ada catatan yang di pilih')

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['text'])
    list_tags.clear()
    list_tags.addItems(notes[key]['tags'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_tags.clear()
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print('Tidak ada catatan yang di pilih')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = search_tag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tags.addItem(tag)
            search_tag.clear()
        with open('notes_data.json', 'w')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print('Tidak ada catatan yang di pilih')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print('Tidak ada catatan yang di pilih')

def search_n_tag():
    tag = search_tag.text()
    if btn_tag_search.text() == 'Search notes by tag'and tag:
        filter = {}
        for note in notes:
            if tag in notes[note]['tags']:
                filter[note] = notes[note]
        btn_tag_search.setText("Reset search")        
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(filter)
    elif btn_tag_search.text() == 'Reset search':
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        search_tag.clear()
        btn_tag_search.setText("Search notes by tag")
        list_notes.addItems(notes)

btn_note_create.clicked.connect(add_note)
btn_note_save.clicked.connect(save_note)
btn_note_delete.clicked.connect(del_note)
list_notes.itemClicked.connect(show_note)
btn_tag_add.clicked.connect(add_tag)
btn_tag_untag.clicked.connect(del_tag)
btn_tag_search.clicked.connect(search_n_tag)

with open('notes_data.json', 'r')as file:
    notes = json.load(file)
list_notes.addItems(notes)


window.show()
app.exec_()
