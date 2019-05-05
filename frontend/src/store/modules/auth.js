import axios from 'axios'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || '',
    user: {},
    successMsg: ''
  },
  getters: {
    isLoggedIn: state => !!state.token,
    getUser: state => state.user,
    getMsg: state => state.successMsg
  },
  mutations: {
    auth_success(state, token) {
      state.token = token
    },
    logout(state) {
      state.token = ''
      state.user = {}
    },
    fetchUser(state, user) {
      state.user = user
    },
    successLoginMsg(state) {
      state.successMsg = 'Pomyślnie zalogowano'
    },
    successLogoutMsg(state) {
      state.successMsg = 'Pomyślnie wylogowano'
    },
    clearMsg(state) {
      state.successMsg = null
    }
  },
  actions: {
    login({commit, dispatch}, loginData) {
      return new Promise ((resolve, reject) => {
        axios.post('/login', {
          username: loginData.username,
          password: loginData.password
        })
        .then( res => {
          const token = res.data.access_token
          localStorage.setItem('token', token)
          localStorage.setItem('refresh_token', res.data.refresh_token)
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
          commit('auth_success', token)
          commit('successLoginMsg')
          dispatch('setRefreshTimer')
          resolve(res)
        }, error => {
          localStorage.removeItem('token')
          reject(error)
        })
      })
    },
    refresh({commit, dispatch}) {
      const refresh = localStorage.getItem('refresh_token')
      axios({
        method: 'post',
        url: '/refresh',
        headers: {'Authorization': 'Bearer ' + refresh}
      })
      .then( res => {
        const token = res.data.access_token
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
        commit('auth_success', token)
        dispatch('setRefreshTimer')
      })
    },
    tryAutoLogin({commit, dispatch, getters}) {
      const token = localStorage.getItem('refresh_token')
      if (!token || getters.isLoggedIn) {
        return
      }
      dispatch('refresh')
    },
    logout({commit, dispatch}) {
      return new Promise((resolve, reject) => {
        axios.post('/logout/access')
        .then(res => {
          localStorage.removeItem('token')
          commit('logout')
          dispatch('logoutRefresh')
        })
        .catch(error => {
          localStorage.removeItem('token')
          commit('logout')
          delete axios.defaults.headers.common['Authorization']
          dispatch('logoutRefresh')
        })
      })
    },
    logoutRefresh({commit}) {
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        return new Promise((resolve, reject) => {
          axios({
            method: 'post',
            url: '/logout/refresh',
            headers: {'Authorization': 'Bearer ' + refresh}
            })
            localStorage.removeItem('refresh_token')
            delete axios.defaults.headers.common['Authorization']
            commit('successLogoutMsg')
            resolve()
        })
      }
    },
    fetchUser({commit}) {
      axios.get('/user')
      .then(res => {
        const user = res.data.user
        commit('fetchUser', user)
      })
      .catch(err => {
        console.log(err)
      })
    },
    setRefreshTimer({commit, dispatch}) {
      setTimeout(() => {
        dispatch('refresh')
      }, 840000)
    }
  }
}
