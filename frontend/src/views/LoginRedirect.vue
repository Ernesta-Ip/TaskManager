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

        const accessToken = response.data.access_token
        const boardId = response.data.board_id

        localStorage.setItem('accessToken', accessToken)
         if (boardId) {
          this.$router.push(`/board/${boardId}`)
        } else {
          this.$router.push('/dashboard')
        }

        } catch (error) {
        console.error('Google login failed:', error)
        this.$router.push('/dashboard')
        }

        

        // Save token and redirect
        //localStorage.setItem('accessToken', response.data.access_token)
        //this.$router.push('/') // or wherever you want to go after login
        //#      board = Board.objects.filter(is_archived=False).order_by('id').first()
        //#      if board:
        //#          return redirect(f'http://localhost:8080/board/{board.id}')
        //#      return redirect('http://localhost:8080/dashboard')
    //   } catch (error) {
    //     console.error('Google login failed:', error)
    //   }
    }
  }
}



</script>
