import Vue from 'vue';
import LoginPage from '../src/login/LoginPage.vue';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';

const localVue = createLocalVue();
localVue.use(Vuex);

let actions;
let store;

beforeEach(() => {
  actions = {
    login: jest.fn(),
    logout: jest.fn()
  };

  store = new Vuex.Store({
    modules: {
      account: {
        namespaced: true,
        state: {
          status: {
            loggingIn: false
          }
        },
        actions
      }
    }
  });
});


it('renders login form', () => {
  const wrapper = shallowMount(LoginPage, { store, localVue });
  expect(wrapper.find('form').exists()).toBe(true);
  expect(wrapper.find('input[name="username"]').exists()).toBe(true);
  expect(wrapper.find('input[name="password"]').exists()).toBe(true);
});


it('shows error messages when fields are empty', async () => {
  const wrapper = shallowMount(LoginPage, { store, localVue });
  await wrapper.find('form').trigger('submit.prevent');

  expect(wrapper.find('.invalid-feedback').exists()).toBe(true);
});

it('calls store action "login" when form is submitted with data', async () => {
  const wrapper = shallowMount(LoginPage, { store, localVue });
  const usernameInput = wrapper.find('input[name="username"]');
  const passwordInput = wrapper.find('input[name="password"]');

  await usernameInput.setValue('testUser');
  await passwordInput.setValue('password');
  await wrapper.find('form').trigger('submit.prevent');

  expect(actions.login).toHaveBeenCalled();
});
