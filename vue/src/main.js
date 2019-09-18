import '@mdi/font/css/materialdesignicons.css';
import axios from 'axios';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import Vue from 'vue';
import VueAxios from 'vue-axios';
import Vuetify from 'vuetify';
import { VAlert, VApp, VAutocomplete, VAvatar, VBtn, VCard, VCheckbox, VChip, VDataIterator, VDataTable, VDatePicker, VDialog, VDivider, VForm, VGrid, VHover, VIcon, VImg, VItemGroup, VList, VMenu, VNavigationDrawer, VPagination, VProgressCircular, VProgressLinear, VSelect, VSlider, VSnackbar, VSubheader, VSwitch, VTabs, VTextarea, VTextField, VTimePicker, VToolbar, VTooltip, VWindow } from 'vuetify/es5/components';
import Resize from 'vuetify/es5/directives';
import colors from 'vuetify/es5/util/colors';
import App from './App';
import router from './router.js';
import store from './store.js';
Vue.config.productionTip = false
Vue.use(Vuetify);
Vue.use(VueAxios, axios)
Vue.use(colors)
Vue.use({
	components: {
		VWindow,
		VItemGroup,
		VSlider,
		VTimePicker,
		VDatePicker,
		VDialog,
		VCheckbox,
		VChip,
		VAlert,
		VImg,
		VProgressCircular,
		VHover,
		VTooltip,
		VTextarea,
		VSubheader,
		VSwitch,
		VApp,
		VNavigationDrawer,
		VGrid,
		VToolbar,
		VList,
		VBtn,
		VAvatar,
		VCard,
		VMenu,
		VIcon,
		VAutocomplete,
		VDataTable,
		VPagination,
		VTabs,
		VSelect,
		VTextField,
		VForm,
		VDivider,
		VProgressLinear,
		VSnackbar,
		VDataIterator,
	},
	directives: {
		Resize,
	},
	iconfont: 'mdi'
});
router.beforeEach((to, from, next) => {
	if (to.matched.some(res => res.meta.NeedLogin)||to.matched.some(res => res.meta.NeedStaff)) {
		if (store.getters.isLogin) {
			next()
		} else {
			next({
				name: 'Login',
				params: { text: "Please Login First" }
			})
		}
	} else if (to.matched.some(res => res.meta.NeedNotLogin)) {
		if (!store.getters.isLogin) {
			next()
		} else {
			next({
				name: 'Error',
				params: { text: "You Has Loginned" }
			})
		}
	} else if (to.matched.some(res => res.meta.NeedStaff)) {
		if (store.getters.IsStaff) {
			next()
		} else {
			next({
				name: 'Error',
				params: { text: "You Are Not Staff" }
			})
		}
	} else {
		next()
	}
});
Vue.use( {
	theme: {
	  primary: colors.red,
	  secondary: colors.grey,
	  accent: colors.black,
	  error: colors.red
	}
  })
new Vue({
	el: '#app',
	router,
	store,
	components: { App },
	template: '<App/>',
})
import 'vuetify/dist/vuetify.min.css'
Vue.prototype.$axios = axios
axios.defaults.withCredentials = true;
