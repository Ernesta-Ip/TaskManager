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

    if (code) {
      try {

        const response = await axios.post('http://localhost:8000/api/v1/auth/google/', {
          code,
          redirect_uri: 'http://localhost:8080/login_redirect_view/',
        })

        console.log('Google login response:', response.data)
        const token = response.data.key 
        const boardId = response.data.board_id
        
        localStorage.setItem('authToken', token)
        
        window.dispatchEvent(new CustomEvent('authToken-localstorage-changed'/*, {
          detail: {
            storage: localStorage.getItem('authToken')
          }
        }*/));

        if (boardId) {
          this.$router.push(`/board/${boardId}`)
        } else {
          this.$router.push('/dashboard')
        }

        } catch (error) {
        console.error('Google login failed:', error)
        this.$router.push('/dashboard')
        }
    }
  }
}
</script>
