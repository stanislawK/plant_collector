import axios from 'axios'

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
    confirmation(context, confId) {
      return new Promise ((resolve, reject) => {
        axios.get('/confirmation/' + confId)
        .then(res => {
          resolve(res);
        }, error => {
          reject(error);
        })
      })
    },
  }
}
