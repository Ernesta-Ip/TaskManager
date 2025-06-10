<template>
  <div>Logging in with Google...</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginRedirect',
  async mounted() {
    const urlParams = new URLSearchParams(window.location.search)
    const code = urlParams.get('code')
    //const state = urlParams.get('state')  // if you're using it

    if (code) {
      try {
        const response = await axios.post('http://localhost:8000/auth/google/', {
          code,
          redirect_uri: 'http://localhost:8080/login_redirect_view/',
        })

        // Save token and redirect
        localStorage.setItem('accessToken', response.data.access_token)
        this.$router.push('/') // or wherever you want to go after login
        //#      board = Board.objects.filter(is_archived=False).order_by('id').first()
        //#      if board:
        //#          return redirect(f'http://localhost:8080/board/{board.id}')
        //#      return redirect('http://localhost:8080/dashboard')
      } catch (error) {
        console.error('Google login failed:', error)
      }
    }
  }
}
</script>
