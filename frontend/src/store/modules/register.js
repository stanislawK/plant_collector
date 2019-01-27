import axios from 'axios'
axios.defaults.baseURL = 'http://0.0.0.0:5000'

export default {
  namespaced: true,
  state: {},
  getters: {},
  mutations: {},
  actions: {
    signup(context, registerData) {
      return new Promise ((resolve, reject) => {
        axios.post('/register', {
          username: registerData.username,
          email: registerData.email,
          password: registerData.password
        })
        .then(res => {
          resolve(res);
        }, error => {
          reject(error);
        })
      })
    },
  }
}
