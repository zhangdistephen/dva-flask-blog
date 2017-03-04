function delay(){
  setTimeout(()=>console.log('delay'),5000)
  console.log('11')
  return {data:'update'}
}
export default {

  namespace: 'example',

  state: {
    token:'init'
  },

  subscriptions: {
    setup({ dispatch, history }) {  // eslint-disable-line
    },
  },

  effects: {
    *update({ payload }, { call, put }) {  // eslint-disable-line
      const {data}=yield call(delay);
      yield put({ type: 'save' ,payload:{token:data}});
      console.log('save')
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
  },

};
