<script>
  import { api } from '@/api';
  import draggable from 'vuedraggable';
  import 'bulma/css/bulma.min.css';

  export default {
    name: 'BoardDetailView',
    components: { draggable },

    mounted() {
        document.addEventListener('click', this.handleClickOutside);
        document.addEventListener('click', this.handleClickOutsideInput);
      },
    
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
        document.removeEventListener('click', this.handleClickOutsideInput);
      },

    data() {
      return {
        activeCard: null,
        hoverCard: null,
        board: {
          name: '',
          id: null,
          lists: [],
        },
        newListName: '',
        showListError: false,
        newCardTitles: {}, 
        todayString: new Date().toISOString().split('T')[0], // "YYYY-MM-DD"
        hoveredListId: null,
        menuOpenListId: null,
        modalRename: {
          isOpen: false,
          listId: null,
          newName: ''
        },
        modalDelete: {
          isOpen: false,
          listId: null,
          name: ''
        },
        modalDeleteCard: {
          isOpen: false,
          cardId: null,
          cardTitle: ''
        },
        modalRenameBoard: {
          isOpen: false,
          newName: ''
        },

        isVisibilityOpen: false,
        isSkipped: localStorage.getItem('skipAuth') === 'true',
      };
    },
    
    created() {
      console.log('Route param:', this.$route.params.id);
      this.fetchBoard(this.$route.params.id);
    },

    watch: {
        '$route.params.id': {
          immediate: true,
          handler(newId) {
            this.fetchBoard(newId);
          }
        }
      },

    methods: {

      goToLogin() {
      localStorage.removeItem('skipAuth');
      this.$router.push({ name: 'Login' });
    },

      visibilityLabel(value) {
        switch (value) {
          case 'private': return 'Private';
          case 'internal': return 'Internal';
          case 'public': return 'Public';
          default: return '';
        }
      },
      visibilityIcon(value) {
        switch (value) {
          case 'private': return 'fas fa-lock';
          case 'internal': return 'fas fa-users';
          case 'public': return 'fas fa-globe';
          default: return '';
        }
      },
      setVisibility(value) {
        this.board.visibility = value;
        this.isVisibilityOpen = false;
        this.updateBoardVisibility(); 
      },

      renameList(list) {
      this.modalRename.isOpen = true;
      this.modalRename.listId = list.id;
      this.modalRename.newName = list.name;
    },
    async submitRename() {
      const id = this.modalRename.listId;
      const name = this.modalRename.newName.trim();
      if (!name) return;
      try {
        const res = await api.patch(`lists/${id}/`, { name });
        const list = this.board.lists.find(l => l.id === id);
        if (list) list.name = res.data.name;
        this.modalRename.isOpen = false;
      } catch (err) {
        console.error('Rename failed:', err);
        alert('Could not rename list.');
      }
    },

     async handleAddList() {
        if (!this.newListName.trim()) {
          this.showListError = true;
          return;
        }
        this.showListError = false;
        await this.addList();
      },

      handleClickOutsideInput(event) {
        const inputEl = this.$refs.newListInput;
        if (inputEl && !inputEl.contains(event.target)) {
          this.showListError = false;
        }
      },

    renameBoard() {
        this.modalRenameBoard.newName = this.board.name;
        this.modalRenameBoard.isOpen = true;
      },

      async submitRenameBoard() {
        const name = this.modalRenameBoard.newName.trim();
        if (!name || name === this.board.name) {
          this.modalRenameBoard.isOpen = false;
          return;
        }

        try {
          const res = await api.patch(`boards/${this.board.id}/`, { name });
          this.board.name = res.data.name;
          this.modalRenameBoard.isOpen = false;
        } catch (err) {
          console.error('Failed to rename board:', err);
          alert('Could not rename board.');
        }
      },
    deleteList(listId) {
      const list = this.board.lists.find(l => l.id === listId);
      if (!list) return;
      this.modalDelete.isOpen = true;
      this.modalDelete.listId = listId;
      this.modalDelete.name = list.name;
    },
    async confirmDelete() {
      const id = this.modalDelete.listId;
      try {
        await api.delete(`lists/${id}/`);
        this.board.lists = this.board.lists.filter(list => list.id !== id);
        this.modalDelete.isOpen = false;
      } catch (err) {
        console.error('Failed to delete list:', err);
        alert('Could not delete list.');
      }
    },

    async confirmDeleteCard() {
        try {
          await api.delete(`cards/${this.modalDeleteCard.cardId}/`);

          for (const list of this.board.lists) {
            list.cards = list.cards.filter(card => card.id !== this.modalDeleteCard.cardId);
          }

          this.modalDeleteCard.isOpen = false;
        } catch (err) {
          console.error('Failed to delete card:', err);
          alert('Could not delete card.');
        }
      },


handleClickOutside(event) {
  if (this.menuOpenListId === null) return;

  const menuRef = this.$refs['dropdown-' + this.menuOpenListId];
  const menuEl = Array.isArray(menuRef) ? menuRef[0] : menuRef;

  if (menuEl && !menuEl.contains(event.target)) {
    this.menuOpenListId = null;
  }
},


        async fetchBoard(boardId) {
          try {
            const res = await api.get(`boards/${boardId}/`);
            console.log('Board data from API:', res.data);
            this.board = {
              ...res.data,
              lists: res.data.lists || []
            };
            for (const list of this.board.lists) {
              list.cards = list.cards || [];
            }
          } catch (err) {
            console.error('Failed to load board:', err);
          }
        },

    
    async addList() {
        try {
          const res = await api.post('lists/', {
            name: this.newListName,
            board: this.board.id,
            order: this.board.lists.length, 
          });
          this.board.lists.push(res.data);
          this.newListName = '';
        } catch (err) {
          console.error('Error adding list:', err);
        }
      },
      
      async addCard(listId) {
        const title = this.newCardTitles[listId];
        if (!title) return;
  
        try {
          const res = await api.post('cards/', {
            title,
            list: listId,
            order: 0, 
          });
          const targetList = this.board.lists.find((l) => l.id === listId);
          targetList.cards.push(res.data);
          this.newCardTitles[listId] = '';
        } catch (err) {
          console.error('Error adding card:', err);
        }
      },
      async onCardDrop() {
        for (const list of this.board.lists) {
          for (let i = 0; i < list.cards.length; i++) {
            const card = list.cards[i];
            await api.patch(`cards/${card.id}/`, {
              order: i,
              list: list.id,
            });
          }
        }
      },
      async onListDrop() {
        for (let i = 0; i < this.board.lists.length; i++) {
          const list = this.board.lists[i];
          await api.patch(`lists/${list.id}/`, {
            order: i,
          });
        }
      },

      async updateBoardVisibility() {
          try {
            const res = await api.patch(`boards/${this.board.id}/`, {
              visibility: this.board.visibility,
            });
            this.board.visibility = res.data.visibility;
          } catch (err) {
            console.error('Failed to update visibility:', err);
          }
        },

        openCard(card) {
              this.activeCard = {
                ...card,
                newComment: '',
                list: card.list,
                comments: card.comments || [],
                membersString: (card.members || []).join(', '),
                attachment: card.attachment || null,
              };

              this.$nextTick(() => {
                const editableDiv = this.$refs.editableTitle;
                if (editableDiv) {
                  editableDiv.textContent = card.title || '';
                }
              });

      },

      closeModal() {
        this.activeCard = null;
      },
      
      async updateCard() {
        try {
          const res = await api.patch(`cards/${this.activeCard.id}/`, {
            title: this.activeCard.title,
            description: this.activeCard.description,
          });

       // find the card and update
        for (const list of this.board.lists) {
          const index = list.cards.findIndex(c => c.id === res.data.id);
          if (index !== -1) {
            list.cards[index] = res.data;
            break;
          }
        }

        this.closeModal();
        } catch (err) {
          console.error('Failed to update card:', err);
        }
      },

      async moveCardToList() {
        try {
          await api.patch(`cards/${this.activeCard.id}/`, {
            list: this.activeCard.list,
          });

         
          const movedCard = { ...this.activeCard };
          
          for (const list of this.board.lists) {
            list.cards = list.cards.filter(c => c.id !== movedCard.id);
          }
          const newList = this.board.lists.find(l => l.id === movedCard.list);
          if (newList) {
            newList.cards.push(movedCard);
          }
        } catch (err) {
          console.error('Failed to move card:', err);
        }
      },

      handleAttachment(event) {
  const file = event.target.files[0];
  this.activeCard.attachment = file;
},

      fileUrl(path) {
        if (!path) return '';
        if (typeof path === 'string') {
          if (path.startsWith('http')) return path;
          return `http://localhost:8001${path}`;
        }
        return '';
      },

        getAttachmentName(attachment) {
          if (!attachment) return '';
          if (typeof attachment === 'string') {
            return attachment.split('/').pop();
          }
          if (attachment instanceof File) {
            return attachment.name;
          }
          return '';
        },

  async saveCardDetails() {
    if (!this.activeCard.title || !this.activeCard.title.trim()) {
    alert('Title cannot be empty.');
    return;
  }

  const datePattern = /^\d{4}-\d{2}-\d{2}$/;

  if (this.activeCard.due_date) {
   
        if (!datePattern.test(this.activeCard.due_date)) {
          alert('Due date must be in DD-MM-YYYY format.');
          return;
        }
      const parsedDate = new Date(this.activeCard.due_date);
        const isValidDate = !isNaN(parsedDate.getTime());
    if (!isValidDate) {
          alert('Invalid date. Please choose a valid due date.');
          return;
        }
      }

  const today = new Date().setHours(0, 0, 0, 0); // текущая дата без времени
  const selectedDate = new Date(this.activeCard.due_date).setHours(0, 0, 0, 0);

  if (this.activeCard.due_date && selectedDate < today) {
    alert('Due date cannot be in the past.');
    return;
  }

  const formData = new FormData();
  formData.append('title', this.activeCard.title);
  formData.append('description', this.activeCard.description);
  formData.append('due_date', this.activeCard.due_date || '');
  const memberList = this.activeCard.membersString
  .split(',')
  .map(e => e.trim())
  .filter(Boolean);

memberList.forEach(email => {
  formData.append('members', email);
});

  if (this.activeCard.attachment) {
    formData.append('attachment', this.activeCard.attachment);
  }

  try {
    const res = await api.patch(`cards/${this.activeCard.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    for (const list of this.board.lists) {
      const idx = list.cards.findIndex(c => c.id === res.data.id);
      if (idx !== -1) {
        list.cards[idx] = res.data;
        break;
      }
    }

    this.closeModal();
  } catch (err) {
  console.error('Failed to save card:', err);

  if (err.response && err.response.data) {
    console.log('Validation error:', err.response.data);
    alert('Validation error: ' + JSON.stringify(err.response.data, null, 2));
  }
}
},
  
        async removeAttachment() {
          if (!this.activeCard || !this.activeCard.id) return;
          const confirmed = confirm('Are you sure you want to remove the attachment?');
          if (!confirmed) return;

          try {
            await api.patch(`cards/${this.activeCard.id}/`, {
              attachment: null,
            });

            this.activeCard.attachment = null; 
          } catch (err) {
            console.error('Failed to remove attachment:', err);
            alert('Could not remove attachment.');
          }
        },

        addComment() {
          if (!this.activeCard.newComment) return;
          this.activeCard.comments.push(this.activeCard.newComment);
          this.activeCard.newComment = '';
        },

        openDeleteCardModal(card) {
          this.modalDeleteCard = {
            isOpen: true,
            cardId: card.id,
            cardTitle: card.title
          };
        },


      async cloneList(originalList) {
        try {
          // 1. new list
          const res = await api.post('lists/', {
            name: originalList.name + ' (copy)',
            board: this.board.id,
            order: this.board.lists.length,
          });
          const newList = res.data;
          newList.cards = [];

          // 2. clone cards (deep copy)
          const clonePromises = originalList.cards.map(card =>
            api.post('cards/', {
              title: card.title,
              description: card.description,
              due_date: card.due_date,
              list: newList.id,
              order: newList.cards.length,
            })
          );

          const cardResponses = await Promise.all(clonePromises);
          newList.cards = cardResponses.map(r => r.data);

          // 3. add to IU
          this.board.lists.push(newList);
        } catch (err) {
          console.error('Failed to clone list:', err);
          alert('Could not clone list.');
        }
      },
    
      
      toggleListMenu(listId) {
            this.menuOpenListId = this.menuOpenListId === listId ? null : listId;
          },

      updateTitleFromContent(event) {
              this.activeCard.title = event.target.textContent.trim();
      }
    },
   }
  

  </script>
  
  <template>

  <div class="container board-container">

  <!-- Board header row: name on left, visibility & members on right -->
  <section class="section pt-3 pb-3">
    <div class="container" style="padding-left: 0;">
      <div class="is-flex is-align-items-center is-flex-wrap-wrap" style="justify-content: space-between; width: 100%;">

    <!-- Left: Board name + edit -->
    <div class="is-flex is-align-items-center mr-4">
      <h1 class="title is-3 has-text-weight-bold has-text-primary mb-0 mr-2">
        {{ board.name }}
      </h1>
      <span
        class="icon is-small has-text-grey is-clickable"
        :class="{ 'is-disabled': isSkipped }"
        :disabled="isSkipped"
        @click="!isSkipped && renameBoard()" 
        title="Edit board name"
      >
        <i class="fas fa-pen"></i>
      </span>
    </div>



<div class="is-flex is-flex-wrap-wrap" style="gap: 1.5rem;">

  <!-- Visibility -->
  <div class="mr-4">
    <label class="label is-size-7 has-text-grey-dark mb-1">Visibility</label>
    <div class="dropdown" :class="{ 'is-active': isVisibilityOpen }">
      <div class="dropdown-trigger">
        <button
          class="invisible-button"
          @click="isVisibilityOpen = !isVisibilityOpen"
          aria-haspopup="true"
          aria-expanded="isVisibilityOpen"
        >
          <div class="is-flex is-align-items-center is-justify-content-space-between">
            <span class="is-size-7 icon is-small mr-2">
              <i :class="visibilityIcon(board.visibility)"></i>
            </span>
            <span class="is-size-7 has-text-grey-dark">{{ visibilityLabel(board.visibility) }}</span>
            <span class="icon is-small ml-2">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </div>
        </button>
      </div>

      <div class="dropdown-menu" role="menu" @click.self="isVisibilityOpen = false">
        <div class="dropdown-content">
          <a v-if="!isSkipped" 
          class="dropdown-item is-size-7 has-text-grey-dark" @click="setVisibility('private')">
            <span class="icon is-small mr-2"><i class="fas fa-lock"></i></span>
            <span>Private</span>
          </a>
          <a v-if="!isSkipped" 
          class="dropdown-item is-size-7 has-text-grey-dark" @click="setVisibility('internal')">
            <span class="icon is-small mr-2"><i class="fas fa-users"></i></span>
            <span>Internal</span>
          </a>
          <a class="dropdown-item is-size-7 has-text-grey-dark" @click="setVisibility('public')">
            <span class="icon is-small mr-2"><i class="fas fa-globe"></i></span>
            <span>Public</span>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Members -->
  <div>
    <label class="label is-size-7 has-text-grey-dark mb-1">Members</label>
    <p class="is-size-7 has-text-grey mt-3">
      {{ board.members?.join(', ') || 'No members assigned' }}
    </p>
  </div>

  <!-- User icon in top-right corner -->
<div v-if="isSkipped" class="is-flex is-align-items-center">
  <button class="button is-rounded is-light is-small has-text-grey" @click="goToLogin" title="Log in to unlock full access">
    <span class="icon is-small">
      <i class="fas fa-user"></i>
    </span>
  </button>
</div>

<!-- Logout button for authenticated users -->
<div v-if="!isSkipped" class="is-flex is-align-items-center">
  <button class="button is-rounded is-light is-small has-text-grey" @click="logout" title="Log out">
    <span class="icon is-small">
      <i class="fas fa-sign-out-alt"></i>
    </span>
  </button>
</div>


</div>

      </div>
    </div>
  </section>
</div>

<!-- Rename Board Modal -->
      <div class="modal" :class="{ 'is-active': modalRenameBoard.isOpen }">
        <div class="modal-background" @click="modalRenameBoard.isOpen = false"></div>
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">Rename Board</p>
            <button class="delete" aria-label="close" @click="modalRenameBoard.isOpen = false"></button>
          </header>
          <section class="modal-card-body">
            <div class="field">
              <label class="label">New name</label>
              <div class="control">
                <input class="input" type="text" v-model="modalRenameBoard.newName" />
              </div>
            </div>
          </section>
          <footer class="modal-card-foot">
            <button class="button is-success" @click="submitRenameBoard">Save</button>
            <button class="button" @click="modalRenameBoard.isOpen = false">Cancel</button>
          </footer>
        </div>
      </div>

  <div class="column">

      <draggable
        v-model="board.lists"
        group="lists"
        item-key="id"
        class="lists"
        @end="onListDrop"
      >

      <!-- Lists -->  
      <template #item="{ element: list }">
          <div>
             <div class="box p-3" :key="list.id">
                <h2 class="subtitle is-6 has-text-weight-bold mb-2 is-flex is-justify-content-space-between">
                  <span>{{ list.name }}</span>
                  <div class="dropdown is-right" :class="{ 'is-active': menuOpenListId === list.id }">
                    <button
                      class="no-style-button "
                      @click.stop="toggleListMenu(list.id)"
                      :aria-expanded="menuOpenListId === list.id"
                    >⋯</button>
                    <div
                      class="dropdown-menu animated-dropdown"
                      role="menu"
                      v-if="menuOpenListId === list.id"
                      @click.stop
                      :ref="'dropdown-' + list.id">
                      <div class="dropdown-content">
                        <a class="dropdown-item is-size-8 has-text-grey-dark has-text-weight-normal dropdown-action" 
                        :class="{ 'is-disabled': isSkipped }"
                        :disabled="isSkipped"
                        @click="!isSkipped && renameList(list)">
                          <span class="icon is-small mr-2"><i class="fas fa-pen fa-sm"></i></span>
                          <span>Rename</span>
                        </a>
                        <a class="dropdown-item is-size-8 has-text-grey-dark has-text-weight-normal dropdown-action" 
                        :class="{ 'is-disabled': isSkipped }"
                        :disabled="isSkipped"
                        @click="!isSkipped && cloneList(list)">
                          <span class="icon is-small mr-2"><i class="fas fa-copy fa-sm"></i></span>
                          <span>Copy</span>
                        </a>
                        <a class="dropdown-item is-size-8 has-text-danger dropdown-action delete-action" 
                        :class="{ 'is-disabled': isSkipped }"
                        :disabled="isSkipped"
                        @click="!isSkipped && deleteList(list.id)">
                          <span class="icon is-small mr-2"><i class="fas fa-trash fa-sm"></i></span>
                          <span>Delete</span>
                        </a>
                      </div>
                    </div>
                  </div>
                </h2>

  
              <!-- Cards -->
              <draggable
                v-model="list.cards"
                group="cards"
                item-key="id"
                @end="onCardDrop"
              >
                <template #item="{ element: card }">
                <li class="card-item">
                <span class="card-title" @click="openCard(card)">
                  {{ card.title }}
                </span>
                <span class="card-icons">
<!-- Edit button -->
<button
  class="button is-small is-white has-text-grey-dark"
  :class="{ 'is-disabled': isSkipped }"
  :disabled="isSkipped"
  @click.stop="!isSkipped && openCard(card)"
  title="Edit"
>
  <span class="icon is-small"><i class="fas fa-pen"></i></span>
</button>

<!-- Delete button -->
<button
  class="button is-small is-white has-text-grey-dark"
  :class="{ 'is-disabled': isSkipped }"
  :disabled="isSkipped"
  @click.stop="!isSkipped && openDeleteCardModal(card)"
  title="Delete"
>
  <span class="icon is-small"><i class="fas fa-trash"></i></span>
</button>


</span>

              </li>
          </template>
              </draggable>
  
              <!-- Form add card -->
              <form @submit.prevent="addCard(list.id)">
                <div class="field has-addons">
                  <div class="control is-expanded">
                    <input
                      v-model="newCardTitles[list.id]"
                      class="input is-small"
                      type="text"
                      placeholder="Add new card"
                    />
                  </div>
                  <div class="control">
                    <button class="button is-small is-light" type="submit" title="Add card">
                      <span class="icon is-small">
                        <i class="fas fa-plus"></i>
                      </span>
                    </button>
                  </div>
                </div>
              </form>
            </div>

            
          </div>
        </template>

              <template #footer>
                <div class="box p-3 has-background-light" style="width: 200px;">
                  <form @submit.prevent="handleAddList">
                    <div class="field has-addons">
                      <div class="control is-expanded">
                        <input
                          ref="newListInput"
                          class="input is-small"
                          :class="{ 'is-danger': showListError }"
                          v-model="newListName"
                          type="text"
                          placeholder="Add new list"
                        />
                      </div>
                      <div class="control">
                        <button class="button is-small is-light" type="submit" title="Add list">
                          <span class="icon is-small">
                            <i class="fas fa-plus"></i>
                          </span>
                        </button>
                      </div>
                    </div>
                    <p v-if="showListError" class="help is-danger">Please fill in this field</p>
                  </form>
                </div>
              </template>
      </draggable>
  </div>
  
  
  
      <!-- Modal window for card -->
       
  <div v-if="activeCard" class="modal is-active">
  <div class="modal-background" @click="closeModal"></div>

  <div class="modal-card">
    <header class="modal-card-head">
          <p class="modal-card-title">
      <span
        class="editable-title"
        contenteditable
        ref="editableTitle"
        @input="updateTitleFromContent"
        @keydown.enter.prevent="saveCardDetails"
      ></span>
    </p>
      <button class="delete" aria-label="close" @click="closeModal"></button>
    </header>

    <section class="modal-card-body">
      <div class="field">
        <label class="label">In list</label>
        <div class="control">
          <div class="select is-fullwidth">
            <select v-model="activeCard.list" @change="moveCardToList">
              <option v-for="list in board.lists" :key="list.id" :value="list.id">
                {{ list.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="field">
        <label class="label">Description</label>
        <div class="control">
          <textarea class="textarea" v-model="activeCard.description" />
        </div>
      </div>

      <div class="field">
        <label class="label">Due Date</label>
        <div class="control">
          <input class="input" type="date" v-model="activeCard.due_date" :min="todayString" @blur="validateDueDate" />
        </div>
      </div>

      <div class="field">
        <label class="label">Attachment</label>
        <div class="control">
          <input class="input" type="file" @change="handleAttachment" />
        </div>
          <div v-if="activeCard.attachment" class="mt-2">
            <a
              :href="fileUrl(activeCard.attachment)"
              :download="getAttachmentName(activeCard.attachment)"  
              target="_blank"
              rel="noopener noreferrer"
              class="has-text-link"
            >
              📎 {{ getAttachmentName(activeCard.attachment) }}
            </a>
            <button class="delete is-small" @click="removeAttachment"></button>
          </div>
      </div>

      <div class="field">
        <label class="label">Members (emails)</label>
        <div class="control">
          <input class="input" v-model="activeCard.membersString" placeholder="user1@example.com, user2@example.com" />
        </div>
      </div>

      <hr />

      <h4 class="title is-6">Comments</h4>
      <ul class="content">
        <li v-for="(comment, idx) in activeCard.comments" :key="idx">{{ comment }}</li>
      </ul>

      <form @submit.prevent="addComment">
        <div class="field has-addons">
          <div class="control is-expanded">
            <input class="input" v-model="activeCard.newComment" placeholder="Add a comment" />
          </div>
          <div class="control">
            <button class="button is-info" type="submit">Add</button>
          </div>
        </div>
      </form>
    </section>

    <footer class="modal-card-foot">
      <button class="button is-success" @click="saveCardDetails">💾 Save</button>
      <button class="button" @click="closeModal">Cancel</button>
    </footer>
  </div>
</div>
      <!-- End of modal window for card -->

      <!-- Delete Card Confirmation Modal -->
      <div class="modal" :class="{ 'is-active': modalDeleteCard.isOpen }">
        <div class="modal-background" @click="modalDeleteCard.isOpen = false"></div>
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">Confirm Deletion</p>
            <button class="delete" aria-label="close" @click="modalDeleteCard.isOpen = false"></button>
          </header>
          <section class="modal-card-body">
            Are you sure you want to delete the card "<strong>{{ modalDeleteCard.cardTitle }}</strong>"?
          </section>
          <footer class="modal-card-foot">
            <button class="button is-danger" @click="confirmDeleteCard">Delete</button>
            <button class="button" @click="modalDeleteCard.isOpen = false">Cancel</button>
          </footer>
        </div>
      </div>

      <!-- Rename List Modal Window -->
          <div class="modal" :class="{ 'is-active': modalRename.isOpen }">
            <div class="modal-background" @click="modalRename.isOpen = false"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Rename List</p>
                <button class="delete" aria-label="close" @click="modalRename.isOpen = false"></button>
              </header>
              <section class="modal-card-body">
                <div class="field">
                  <label class="label">New name</label>
                  <div class="control">
                    <input class="input" type="text" v-model="modalRename.newName" />
                  </div>
                </div>
              </section>
              <footer class="modal-card-foot">
                <button class="button is-success" @click="submitRename">Save</button>
                <button class="button" @click="modalRename.isOpen = false">Cancel</button>
              </footer>
            </div>
          </div>

          <!-- Delete List Confirmation Modal -->
          <div class="modal" :class="{ 'is-active': modalDelete.isOpen }">
            <div class="modal-background" @click="modalDelete.isOpen = false"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Confirm Deletion</p>
                <button class="delete" aria-label="close" @click="modalDelete.isOpen = false"></button>
              </header>
              <section class="modal-card-body">
                Are you sure you want to delete the list "{{ modalDelete.name }}"?
              </section>
              <footer class="modal-card-foot">
                <button class="button is-danger" @click="confirmDelete">Delete</button>
                <button class="button" @click="modalDelete.isOpen = false">Cancel</button>
              </footer>
            </div>
          </div>
  </template>
  
  <style>

  
  
  .lists {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  align-items: flex-start;
  }

 .card-item {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-radius: 4px;
  padding: 0.3rem 0.5rem;
  margin-bottom: 0.3rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.card-item:hover .card-icons {
  visibility: visible;
}

.card-icons button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
}

.list-header:hover .delete-button {
  visibility: visible; /* показывается при наведении */
}


.comments {
  padding-left: 1rem;
  margin-bottom: 1rem;
}

.editable-title {
  outline: none;
  padding: 0.3rem 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 4px;
  background-color: #f7f7f7;
  cursor: text;
}

.editable-title:focus {
  background-color: #fffbe6;
  border: 1px solid #ccc;
}

.editable-title {
  direction: ltr; /* 👈 гарантирует, что текст вводится слева направо */
}

@media (max-width: 768px) {
  .lists {
    flex-direction: column;
    align-items: stretch;
    padding-left: 68px; 
  }

  .list {
    width: 100%;
    margin-bottom: 1rem;
    padding-left: 68px; 
  }

  .add-list {
    width: 100%;
  }


}

.card-details input,
.card-details textarea,
.card-details select,
button {
  font-size: 1rem;
}

input,
textarea,
select {
  max-width: 100%;
}

.modal.is-active {
  display: flex !important;
  align-items: center;
  justify-content: center;
}
.no-style-button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}
.no-style-button:hover {
  color: #000;
}

.animated-dropdown {
  animation: fadeIn 0.15s ease-out;
  transition: opacity 0.2s ease, transform 0.2s ease;
  transform-origin: top right;
}

.modal-card-foot {
  justify-content: flex-end;
  gap: 0.5rem;
}

.card-icons {
  display: flex;
  gap: 0rem;
  opacity: 0;
  transform: translateY(-2px);
  transition: opacity 0.25s ease-in-out, transform 0.25s ease-in-out;
}

.card-item:hover .card-icons {
  opacity: 1;
  transform: translateY(0);
}

button.is-disabled {
  pointer-events: none;
  opacity: 0.5;
  cursor: not-allowed;
}
.board-container {
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (max-width: 768px) {
  .board-container {
    padding-left: 68px; 
  }
}




@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

  </style>
  