import axios from 'axios'

export default {
  namespaced: true,
  state: {
    plant_id: '',
    uploadProgress: 0
  },
  getters: {
    progress: state => state.uploadProgress
  },
  mutations: {
    setPlantId (state, plant_id) {
      state.plant_id = plant_id
    },
    cleanPlantState (state) {
      state.plant_id = ''
    },
    setProgress (state, progress) {
      state.uploadProgress = progress
    }
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
    addImage({state, commit}, imgData) {
      const config = {
        onUploadProgress: uploadEvent => {
          const progress = Math.round(uploadEvent.loaded / uploadEvent.total * 100)
          commit('setProgress', progress)
        }
      }
      return new Promise ((resolve, reject) => {
        axios.post('/plant/' + state.plant_id + '/upload/image',
          imgData,
          config,
          { headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': '*'
          }
        })
        .then(res => {
          resolve(res);
        }, error => {
          reject(error);
        })
      })
    },
    getPlant({commit}, plant_id) {
      return new Promise ((resolve, reject) => {
        axios.get('/plant/' + plant_id)
        .then(res => {
          resolve(res);
        }, error => {
          console.log(error)
          reject(error);
        })
      })
    },
    getImage({commit}, plant_id) {
      return new Promise ((resolve, reject) => {
        axios.get('/plant/' + plant_id + '/image',
        { headers: {
          'Content-Type': 'multipart/form-data',
          'Access-Control-Allow-Origin': '*'
        },
        responseType: 'arraybuffer'
      })
      .then(res => {
        resolve(res)
      }, error => {
        console.log(error)
        reject(error)
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
