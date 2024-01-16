import { writable } from 'svelte/store';

function create_loggedin_user_store() {
    const { subscribe, set, update } = writable(null);
    return {
        subscribe,
        set,
        update,
        login: (user) => {
            set(user)
        },
        logout: () => {
            set("")
        }
    };
}

export const loged_user = create_loggedin_user_store();