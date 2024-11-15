<script setup lang="ts">
    const { status, data, signOut } = useAuth();

    const drawer = ref(false);
    const topNavItems = ref([
        { title: 'Home', icon: 'mdi-home', href: '/' },
        { title: 'Chores', icon: 'mdi-format-list-bulleted', href: '/chores' },
        { title: 'Tools', icon: 'mdi-wrench', href: '/tools' },
        { title: 'Calendar', icon: 'mdi-calendar', href: '/calendar' },
    ]);

    const bottomNavItems = ref([
        { title: 'Settings', icon: 'mdi-cog', href: '/settings' },
    ]);
</script>

<template>
    <v-app-bar color="primary" prominent>
        <v-app-bar-nav-icon
        variant="text"
        @click.stop="drawer = !drawer"
        ></v-app-bar-nav-icon>

        <v-toolbar-title>GopherDen</v-toolbar-title>

        <v-btn right icon="mdi-dots-vertical" variant="text"></v-btn>
    </v-app-bar>

    <v-navigation-drawer
        v-model="drawer"
        app
    >
        <v-list dense nav>
            <v-list-item v-for="item in topNavItems" :key="item.title" :to="item.href" :prepend-icon="item.icon" link>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
        </v-list>
        <template v-slot:append>
            <v-list dense nav>
                <template v-if="status === 'authenticated'">
                    <v-list-item v-for="item in bottomNavItems" :key="item.title" :to="item.href" :prepend-icon="item.icon" link>
                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="signOut({ callbackUrl: '/login' })" prepend-icon="mdi-logout" link>
                        <v-list-item-title>Logout</v-list-item-title>
                    </v-list-item>
                </template>
                <v-list-item v-if="status === 'unauthenticated'" to="/login" prepend-icon="mdi-login" link>
                    <v-list-item-title>Login</v-list-item-title>
                </v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>

  