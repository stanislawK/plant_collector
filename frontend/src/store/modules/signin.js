import axios from 'axios'
axios.defaults.baseURL = 'http://0.0.0.0:5000'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || '',
    user: {}
  },
  getters: {
    isLoggedIn: state => !!state.token,
  },
  mutations: {
    auth_success(state, token) {
      state.token = token
    }
  },
  actions: {
    login({commit}, loginData) {
      return new Promise ((resolve, reject) => {
        axios.post('/login', {
          username: loginData.username,
          password: loginData.password
        })
        .then( res => {
          localStorage.setItem('token', res.data.access_token)
          localStorage.setItem('refresh_token', res.data.refresh_token)
          commit('auth_success', res.data.access_token)
          resolve(res)
        }, error => {
          localStorage.removeItem('token')
          reject(error)
        })
      })
    },
    tryAutoLogin({commit}) {
      const token = localStorage.getItem('token')
      if (!token) {
        return
      }
      commit('auth_success', token)
    }
  }
}
