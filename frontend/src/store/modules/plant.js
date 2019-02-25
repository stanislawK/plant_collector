import axios from 'axios'

export default {
  namespaced: true,
  state: {
    plant_id: '',
  },
  getters: {},
  mutations: {
    setPlantId (state, plant_id) {
      state.plant_id = plant_id
    },
    cleanPlantState (state) {
      state.plant_id = '',
    },
  },
  actions: {
    addName({commit}, plantNameData) {
      return new Promise ((resolve, reject) => {
        axios.post('/plant', {
          name: plantNameData.name,
          latin: plantNameData.latin,
          difficulty: plantNameData.difficulty
        })
        .then(res => {
          commit('setPlantId', res.data.plant_id);
          resolve(res);
        }, error => {
          reject(error);
        })
      })
    },
    addDesc({state}, descData) {
      return new Promise ((resolve, reject) => {
        axios.post('/plant/' + state.plant_id + '/description', {
          content: descData.description,
          source: descData.source
        })
        .then(res => {
          resolve(res);
        }, error => {
          reject(error);
        })
      })
    },
    deletePlant({commit, state}) {
      return new Promise ((resolve, reject) => {
        axios.delete('/plant/' + state.plant_id)
        .then(res => {
          commit('cleanPlantState');
          resolve(res);
        }, error => {
          reject(error)
        });
      })
    }

  }
}
