<template>
  <div class="app">
 
<!-- Burger menu -->
<div class="burger-container" v-if="isSidebarHidden">
  <button class="menu-toggle" @click="toggleSidebar">
    <span class="icon"><i class="fas fa-bars"></i></span>
  </button>
</div>


<div v-if="showBoardModal" class="modal is-active">
  <div class="modal-background" @click="closeBoardModal"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Create New Board</p>
      <button class="delete" aria-label="close" @click="closeBoardModal"></button>
    </header>

    <section class="modal-card-body">
      <form @submit.prevent="createBoard">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input class="input" v-model="newBoardName" required />
          </div>
        </div>

        <div class="field">
          <label class="label">Visibility</label>
          <div class="control">
            <div class="select is-fullwidth">
            <select v-model="newBoardVisibility">
              <option value="public">Public</option>
              <option v-if="!isSkipped" value="internal">Internal</option>
              <option v-if="!isSkipped" value="private">Private</option>
            </select>
            </div>
          </div>
        </div>

        <div class="field">
          <label class="label">Members (emails, comma separated)</label>
          <div class="control">
            <textarea
              class="textarea"
              v-model="newBoardMembers"
              placeholder="user1@example.com, user2@example.com"
            ></textarea>
          </div>
        </div>
      </form>
    </section>

    <footer class="modal-card-foot">
      <button class="button is-success" @click="createBoard">Create</button>
      <button class="button" @click="closeBoardModal">Cancel</button>
    </footer>
  </div>
</div>


    <aside
     v-if="$route.name !== 'Login' && !isSidebarHidden"
      class="menu has-background-light px-5 py-5"
      :style="{ width: sidebarWidth + 'px' }"
    >
    
    <!-- Boards -->

    <div class="sidebar-header mb-3" @click="toggleBoardList">
<div class="px-3 py-2">
  <button
    class="button is-small is-light is-fullwidth"
    @click="goToLogin"
  >
    <span class="icon is-small">
      <i class="fas fa-arrow-left"></i>
    </span>
    <span>Back to Login</span>
  </button>
</div>

    <span class="menu-label">Boards</span>
      <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
      
    </div>
        <ul v-if="showBoardList" class="board-list">
        <li
            v-for="board in activeBoards"
            :key="board.id"
          class="board-item"
          :class="{ active: board.id === selectedBoardId }"
          @mouseenter="hoveredBoardId = board.id"
          @mouseleave="handleMouseLeave(board.id)"
        >
          <span class="board-name" @click="goToBoardFromList(board.id)">
            {{ board.name }}
          </span>

          <!-- Drop-down menu -->
          <div class="dropdown is-active">
          <div class="dropdown-trigger"></div>
          
          <!-- Button ⋯ -->
          <div class="board-menu-wrapper" v-if="hoveredBoardId === board.id">
            <button class="board-options-toggle" @click.stop="toggleMenu(board.id)">⋯</button>
          </div>
          <div
            v-if="menuOpenBoardId === board.id"
            class="dropdown-menu animated-dropdown"
            role="menu"
            @click.stop
            :ref="'dropdown-' + board.id"
          >
            <div class="dropdown-content">
              <a
                class="dropdown-item is-size-8 has-text-grey-dark has-text-weight-normal dropdown-action"
                :class="{ 'is-disabled': isSkipped }"
                :disabled="isSkipped"
                @click="!isSkipped && openRenameModal(board)"
              >
                <span class="icon is-small mr-2"><i class="fas fa-pen fa-sm"></i></span>
                <span>Rename</span>
              </a>

              <a
                v-if="!board.is_archived"
                class="dropdown-item is-size-8 has-text-grey-dark has-text-weight-normal dropdown-action"
                :disabled="isSkipped"
                @click="!isSkipped && openArchiveModal(board)"
                
              >
                <span class="icon is-small mr-2"><i class="fas fa-box fa-sm"></i></span>
                <span>Archive</span>
              </a>

              <a
                v-if="board.is_archived"
                class="dropdown-item is-size-8 has-text-grey-dark has-text-weight-normal dropdown-action"
                :disabled="isSkipped"
                @click="!isSkipped && openRestoreBoard(board)"
                
              >
                <span class="icon is-small mr-2"><i class="fas fa-undo fa-sm"></i></span>
                <span>Restore</span>
              </a>

              <a
                class="dropdown-item is-size-8 has-text-danger dropdown-action delete-action"
                :disabled="isSkipped"
                @click="!isSkipped && openDeleteModal(board)"
              >
                <span class="icon is-small mr-2"><i class="fas fa-trash fa-sm"></i></span>
                <span>Delete</span>
              </a>
            </div>
          </div>
          </div>
        </li>
      </ul>

    <!-- Add new board button-->
      <button class="button is-fullwidth is-small is-light mt-4" @click="showBoardModal = true">
          + New Board
        </button>

    <!-- Archived Boards-->
      <div class="sidebar-header mt-5" @click="toggleArchived">
        <span class="menu-label">Archived Boards</span>
        <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
      </div>


        <ul v-if="showArchived" class="board-list archived">
          <li
  v-for="board in archivedBoards"
  :key="board.id"
  class="board-item"
  @mouseenter="hoveredBoardId = board.id"
  @mouseleave="handleMouseLeave(board.id)"
>
    <span
      class="board-name"
      @click="goToBoardFromList(board.id)"
    >
      {{ board.name }}
    </span>

<div class="dropdown is-right" :class="{ 'is-active': menuOpenBoardId === board.id }">
  <div class="dropdown-trigger board-menu-wrapper">
    <button
      class="board-options-toggle"
      @click.stop="toggleMenu(board.id)"
      :class="{ 'is-visible': hoveredBoardId === board.id || menuOpenBoardId === board.id }"
    >
      ⋯
    </button>
  </div>

  <div
    class="dropdown-menu animated-dropdown"
    role="menu"
    v-if="menuOpenBoardId === board.id"
    :ref="'dropdown-' + board.id"
    @click.self.stop
  >
    <div class="dropdown-content">
      <a class="dropdown-item" @click="openRenameModal(board)">
        <span class="icon is-small mr-2"><i class="fas fa-pen fa-sm"></i></span>
        <span>Rename</span>
      </a>
      <a
        v-if="!board.is_archived"
        class="dropdown-item"
        @click="openArchiveModal(board)"
      >
        <span class="icon is-small mr-2"><i class="fas fa-box fa-sm"></i></span>
        <span>Archive</span>
      </a>
      <a
        v-if="board.is_archived"
        class="dropdown-item"
        @click="restoreBoard(board)"
      >
        <span class="icon is-small mr-2"><i class="fas fa-undo fa-sm"></i></span>
        <span>Restore</span>
      </a>
      <a
        class="dropdown-item has-text-danger"
        @click="openDeleteModal(board)"
      >
        <span class="icon is-small mr-2"><i class="fas fa-trash fa-sm"></i></span>
        <span>Delete</span>
      </a>
    </div>
  </div>
</div>

</li>

        </ul>
</aside>

      <!-- Resizer -->
      <div
      v-if="$route.name !== 'Login'"
        class="resizer"
        :style="{ left: sidebarWidth + 'px' }"
        @mousedown="startResizing"
      ></div>

      <!-- Create Board Modal -->
    <div v-if="showBoardModal" class="modal is-active">
      <div class="modal-background" @click="closeBoardModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Create New Board</p>
          <button class="delete" aria-label="close" @click="closeBoardModal"></button>
        </header>
        <section class="modal-card-body">
          <form @submit.prevent="createBoard">
            <div class="field">
              <label class="label">Name</label>
              <div class="control">
                <input class="input" v-model="newBoardName" required />
              </div>
            </div>
            <div class="field">
              <label class="label">Visibility</label>
              <div class="control">
                <div class="select is-fullwidth">
                  <select v-model="newBoardVisibility">
                    <option value="public">Public</option>
                    <option v-if="!isSkipped" value="internal">Internal</option>
                    <option v-if="!isSkipped" value="private">Private</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="field">
              <label class="label">Members (emails, comma separated)</label>
              <div class="control">
                <textarea class="textarea" v-model="newBoardMembers" placeholder="user1@example.com, user2@example.com"></textarea>
              </div>
            </div>
          </form>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="createBoard">Create</button>
          <button class="button" @click="closeBoardModal">Cancel</button>
        </footer>
      </div>
    </div>

    
        <!-- Rename Modal -->
        <div v-if="showRenameModal" class="modal is-active">
          <div class="modal-background" @click="closeRenameModal"></div>
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Rename Board</p>
              <button class="delete" aria-label="close" @click="closeRenameModal"></button>
            </header>
            <section class="modal-card-body">
              <input class="input" v-model="renameBoardName" placeholder="New board name" />
            </section>
            <footer class="modal-card-foot">
              <button class="button is-success" @click="confirmRenameBoard">Rename</button>
              <button class="button" @click="closeRenameModal">Cancel</button>
            </footer>
          </div>
        </div>


    <!-- Archive Modal -->
    <div v-if="showArchiveModal" class="modal is-active">
      <div class="modal-background" @click="closeArchiveModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Archive Board</p>
          <button class="delete" aria-label="close" @click="closeArchiveModal"></button>
        </header>
        <section class="modal-card-body">
          Are you sure you want to archive board <strong>{{ selectedBoard?.name }}</strong>?
        </section>
        <footer class="modal-card-foot">
          <button class="button is-warning" @click="confirmArchiveBoard">Archive</button>
          <button class="button" @click="closeArchiveModal">Cancel</button>
        </footer>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal is-active">
      <div class="modal-background" @click="openDeleteModal(board)"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Delete Board</p>
          <button class="delete" aria-label="close" @click="closeDeleteModal"></button>
        </header>
        <section class="modal-card-body">
          Are you sure you want to permanently delete board <strong>{{ selectedBoard?.name }}</strong>?
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirmDeleteBoard">Delete</button>
          <button class="button" @click="closeDeleteModal">Cancel</button>
        </footer>
      </div>
    </div>




    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>

import { api } from '@/api';
import { useRouter } from 'vue-router';

export default {
   setup() {
    const router = useRouter();
    return { router };
  },
  name: 'App',
   
  data() {
    return {
      boards: [],
      hoveredBoardId: null,
      menuOpenBoardId: null,
      selectedBoardId: '',
      selectedBoard: null,
      showBoardList: true,
      showArchived: false,
      isSidebarHidden: window.innerWidth < 768,
      showBoardModal: false,
      showRenameModal: false,
      showDeleteModal: false,
      showArchiveModal: false,
      renameBoardName: '',
      newBoardName: 'Untitled Board',
      newBoardVisibility: 'private',
      newBoardMembers: '',
      sidebarWidth: 240,
      isResizing: false,
      isSkipped: localStorage.getItem('skipAuth') === 'true',
    };
  },

  computed: {
    archivedBoards() {
      if (this.isSkipped) {
        return this.boards.filter(b => b.is_archived && b.visibility === 'public');
      }
      return this.boards.filter(b => b.is_archived);
    },
    activeBoards() {
      if (this.isSkipped) {
        return this.boards.filter(b => !b.is_archived && b.visibility === 'public');
      }
      return this.boards.filter(b => !b.is_archived);
    }
  },

  async created() {
    try {
      const res = await api.get('boards/');
      this.boards = res.data;

      const currentId = this.$route.params.id;
      if (currentId) {
        this.selectedBoardId = currentId;
      }
    } catch (err) {
      console.error('Failed to load boards:', err);
    }
  },

  watch: {
    '$route.params.id'(newId) {
      this.selectedBoardId = newId;
    }
  },

  mounted() {
    this.updateSidebarVisibility();
    window.addEventListener('resize', this.updateSidebarVisibility);
    window.addEventListener('mousemove', this.resizeSidebar);
    window.addEventListener('mouseup', this.stopResizing);
    document.addEventListener('click', this.handleClickOutside);
    this.isSkipped = localStorage.getItem('skipAuth') === 'true';
  },

  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },

  methods: {
    goToLogin() {
      localStorage.removeItem('skipAuth');
      this.$router.push({ name: 'Login' });
    },

    logout() {
    localStorage.removeItem('skipAuth');
    window.location.href = 'http://localhost:8001/accounts/logout/';
    },

    updateSidebarVisibility() {
      this.isSidebarHidden = window.innerWidth < 768;
    },
    startResizing() {
      this.isResizing = true;
    },
    resizeSidebar(e) {
      if (!this.isResizing) return;
      const minWidth = 150;
      const maxWidth = 500;
      const newWidth = e.clientX;
      this.sidebarWidth = Math.min(Math.max(newWidth, minWidth), maxWidth);
    },
    stopResizing() {
      this.isResizing = false;
    },
    toggleMenu(boardId) {
      this.menuOpenBoardId = this.menuOpenBoardId === boardId ? null : boardId;
    },
    toggleArchived() {
      this.showArchived = !this.showArchived;
    },
    handleClickOutside(event) {
      if (!this.menuOpenBoardId) return;
      const menuRefs = this.$refs['dropdown-' + this.menuOpenBoardId];
      const menuRef = Array.isArray(menuRefs) ? menuRefs[0] : menuRefs;

      if (!menuRef || !menuRef.contains(event.target)) {
        this.menuOpenBoardId = null;
      }
    },
    handleMouseLeave(boardId) {
      if (this.menuOpenBoardId !== boardId) {
        this.hoveredBoardId = null;
      }
    },
    openRenameModal(board) {
      this.selectedBoard = board;
      this.renameBoardName = board.name;
      this.showRenameModal = true;
    },
    closeRenameModal() {
      this.showRenameModal = false;
      this.renameBoardName = '';
    },

    confirmRenameBoard() {
  if (!this.renameBoardName.trim()) return;
  api.patch(`boards/${this.selectedBoard.id}/`, { name: this.renameBoardName.trim() })
    .then(res => {
      // Обновим в selectedBoard
      this.selectedBoard.name = res.data.name;
      // Обновим в boards
      const idx = this.boards.findIndex(b => b.id === this.selectedBoard.id);
      if (idx !== -1) {
        this.boards[idx].name = res.data.name;
      }
      this.showRenameModal = false;
    })
    .catch(err => {
      console.error('Rename failed:', err);
    });
},

    openDeleteModal(board) {
      this.selectedBoard = board;
      this.showDeleteModal = true;
    },
    confirmDeleteBoard() {
      api.delete(`boards/${this.selectedBoard.id}/`)
        .then(() => {
          this.boards = this.boards.filter(b => b.id !== this.selectedBoard.id);
          if (this.selectedBoardId === this.selectedBoard.id) {
            this.$router.push('/');
          }
          this.showDeleteModal = false;
        })
        .catch(err => {
          console.error('Delete failed:', err);
        });
    },

    closeDeleteModal() {
  this.showDeleteModal = false;
  this.selectedBoard = null;
}, 

    openArchiveModal(board) {
      this.selectedBoard = board;
      this.showArchiveModal = true;
    },
      confirmArchiveBoard() {
        api.patch(`boards/${this.selectedBoard.id}/`, { is_archived: true })
          .then(res => {
           
            const idx = this.boards.findIndex(b => b.id === this.selectedBoard.id);
            if (idx !== -1) {
              this.boards[idx] = res.data;
            }

            if (this.selectedBoardId === this.selectedBoard.id) {
              this.$router.push('/');
            }

            this.showArchiveModal = false;
          })
          .catch(err => {
            console.error('Archiving failed:', err);
          });
      },

    closeArchiveModal() {
      this.showArchiveModal = false;
    },


    restoreBoard(board) {
      api.patch(`boards/${board.id}/`, { is_archived: false })
        .then(res => {
          Object.assign(board, res.data);
        })
        .catch(err => {
          console.error('Restore failed:', err);
        });
    },
    toggleBoardList() {
      this.showBoardList = !this.showBoardList;
    },
    toggleSidebar() {
      this.isSidebarHidden = !this.isSidebarHidden;
    },
    closeBoardModal() {
      this.showBoardModal = false;
      this.newBoardName = 'Untitled Board';
      this.newBoardVisibility = 'private';
      this.newBoardMembers = '';
    },
    goToBoardFromList(boardId) {
      this.selectedBoardId = boardId;
      this.$router.push(`/board/${boardId}`);
      if (window.innerWidth < 768) {
        this.isSidebarHidden = true;
      }
    },
    async createBoard() {
      if (this.isSkipped) {
        this.newBoardVisibility = 'public';
      }
      try {
        const res = await api.post('boards/', {
          name: this.newBoardName,
          visibility: this.newBoardVisibility,
          members: this.newBoardMembers
            .split(',')
            .map(email => email.trim())
            .filter(email => email),
        });

        this.boards.push(res.data);
        this.selectedBoardId = res.data.id;
        this.$router.push(`/board/${res.data.id}`);
        this.closeBoardModal();
      } catch (err) {
        console.error('Failed to create board:', err);
      }
    }
  },
};
</script>



<style>
.app {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow: auto;
}

select {
  width: 100%;
  padding: 0.4rem;
}

  .resizer {
  position: absolute;
  width: 5px;
  cursor: ew-resize;
  background: transparent;
  height: 100vh;
  z-index: 1000;
}

.board-list li {
  padding: 0.4rem 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  color: #333;
  transition: background 0.2s;
}

.board-list li:hover {
  background-color: #e0e0e0;
}

.board-list li.active {
  background-color: #d0d0d0;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 1rem;
  visibility: hidden;
}

.board-item:hover .delete-btn {
  visibility: visible;
}

.board-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.board-menu-wrapper {
  position: relative;
  margin-left: 0.5rem;
  flex-shrink: 0; 
}

.board-options-toggle {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #555;
  padding: 0;
  line-height: 1;
}

.menu-toggle {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #555;
}

.context-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.3rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  min-width: 120px;
}

.context-menu button {
  display: block;
  width: 100%;
  padding: 0.4rem 0.8rem;
  background: none;
  border: none;
  text-align: left;
  font-size: 0.9rem;
  cursor: pointer;
}

.context-menu button:hover {
  background-color: #f0f0f0;
}

.is-hidden-desktop {
  display: none !important;
}

.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  left: auto !important;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 100;
  min-width: 140px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.board-menu-wrapper {
  position: relative;
  margin-left: 0.5rem;
}

.animated-dropdown {
  animation: fadeIn 0.15s ease-in-out;
  z-index: 20;
}
.board-options-toggle {
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}
.board-item:hover .board-options-toggle,
.board-options-toggle.is-visible {
  opacity: 1;
  pointer-events: auto;
}

.burger-container {
  position: fixed;
  top: 2rem;
  left: 1rem;
  /* width: 68px; */
  display: flex;
  justify-content: flex-start;
  padding-left: 0.1rem;
  padding-right: 0.1rem;
  z-index: 1000;
}


.menu-toggle {
  background: #ffffff;
  border: 1px solid #ddd;
  padding: 0.5rem;
  border-radius: 8px;
  font-size: 1.5rem;
  cursor: pointer;
  color: #555;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: background 0.2s ease;
}

.menu-toggle:hover {
  background: #f5f5f5;
}


@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1023px) {
  .is-hidden-desktop {
    display: inline-block !important;
  }
}





</style>
