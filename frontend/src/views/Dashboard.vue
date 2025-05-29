<script>
import { api } from '@/api';

export default {
  name: 'DashboardView',
  data() {
    return {
      boards: [],
      // newBoardName: '',
      // newBoardVisibility: 'private',
      // isSkipped: false,
    };
  },
  async mounted() {
    try {
          const response = await api.get('boards/');
          this.boards = response.data;
          const firstActive = this.boards.find(b => !b.is_archived);
          if (firstActive) {
            this.$router.replace({ name: 'BoardDetail', params: { id: firstActive.id } });
          }
        } catch (err) {
          console.error('Failed to fetch boards', err);
        }
  }
};
</script>
