/**
 * Created by stephenzhang on 2017/3/4.
 */

export default {

  namespace: 'example2',

  state: {},

  subscriptions: {
    setup({ dispatch, history }) {
      dispatch({type:'zaifetch'})// eslint-disable-line
    },
  },

  effects: {
    *fetch({ payload }, { call, put,select }) {  // eslint-disable-line
      var token=yield select(state=>state.example.token);
      console.log(token);
      yield put({type:'example/update'});


      yield put({ type: 'save' });
      return {status:'ok'}
    },
    *zaifetch({},{put,call,select}){
      const {status}= yield put({type:'fetch'});
      console.log(status)
      var token=yield select(state=>state.example.token);
      console.log(token);
    }
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
  },

};
