import Vue from 'vue';
import Vuex from 'vuex';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import HomePage from '../src/home/HomePage.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('HomePage.vue', () => {
    let actions;
    let store;
    let state;

    beforeEach(() => {
        actions = {
            getAll: jest.fn(),
            delete: jest.fn()
        };

        state = {
            account: {
                user: { firstName: 'TestUser' } // Mock the user object
            },
            users: {
                all: {
                    loading: false,
                    error: null,
                    items: [{ id: 1, firstName: 'User', lastName: 'One' }]
                }
            }
        };

        store = new Vuex.Store({
            modules: {
                account: {
                    namespaced: true,
                    state: state.account, // Include account state
                },
                users: {
                    namespaced: true,
                    actions,
                    state: state.users,
                }
            }
        });
    });

    it('renders user greeting and users list', () => {
        const wrapper = shallowMount(HomePage, { store, localVue });

        expect(wrapper.find('h1').text()).toBe('Hi TestUser!');
        expect(wrapper.findAll('li').length).toBe(1);
        expect(wrapper.find('li').text()).toContain('User One');
    });

    it('dispatches "getAllUsers" action on creation', () => {
        shallowMount(HomePage, { store, localVue });
        expect(actions.getAll).toHaveBeenCalled();
    });

    it('calls "deleteUser" action when delete link is clicked', async () => {
        const wrapper = shallowMount(HomePage, { store, localVue });
        await wrapper.find('a.text-danger').trigger('click');
        expect(actions.delete).toHaveBeenCalled();
    });

});
