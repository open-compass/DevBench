import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import VeeValidate from 'vee-validate';
import RegisterPage from '../src/register/RegisterPage.vue';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(VeeValidate);

let actions;
let store;

beforeEach(() => {
    actions = {
        register: jest.fn()
    };

    store = new Vuex.Store({
        modules: {
            account: {
                namespaced: true,
                state: {
                    status: { registering: false }
                },
                actions
            }
        }
    });
});

describe('RegisterPage.vue', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(RegisterPage, {
            store,
            localVue,
            sync: false
        });
    });

    it('renders registration form', () => {
        const wrapper = shallowMount(RegisterPage, { store, localVue });
        expect(wrapper.find('form').exists()).toBe(true);
        expect(wrapper.find('input[name="firstName"]').exists()).toBe(true);
        expect(wrapper.find('input[name="lastName"]').exists()).toBe(true);
        expect(wrapper.find('input[name="username"]').exists()).toBe(true);
        expect(wrapper.find('input[name="password"]').exists()).toBe(true);
    });

    it('shows error messages for empty required fields', async () => {
        const wrapper = shallowMount(RegisterPage, { store, localVue });

        // Optionally set invalid data or leave fields empty
        wrapper.setData({
            user: {
                firstName: '',
                lastName: '',
                username: '',
                password: ''
            }
        });

        // Trigger form submission
        wrapper.find('form').trigger('submit.prevent');

        // Wait for Vue's nextTick to allow all async updates to finish
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        // Now check for the existence of the error feedback
        expect(wrapper.find('.invalid-feedback').exists()).toBe(true);
    });


    it('calls store action "register" when form is submitted with valid data', async () => {
        wrapper.setData({
            user: {
                firstName: 'Test',
                lastName: 'User',
                username: 'testuser',
                password: 'password'
            }
        });

        // Mock the validation to always pass
        wrapper.vm.$validator.validate = jest.fn().mockResolvedValue(true);

        wrapper.find('form').trigger('submit.prevent');
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.$validator.validate).toHaveBeenCalled();
        expect(actions.register).toHaveBeenCalled();
    });
});
