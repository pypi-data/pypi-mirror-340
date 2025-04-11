import { h, onMounted, ref, computed, watch } from "vue";
import hljs from 'highlight.js/lib/core.min.js'

async function registerLanguage(language) {
  const langModule = await import(`highlight.js/languages/${language}.min.js`);
  hljs.registerLanguage(language, langModule.default);
}


export default {
  props: ['code', 'language'],
  setup(props) {
    const language = ref(props.language ?? hljs.getLanguage(props.code))

    watch(() => props.language, (newLanguage) => {
      language.value = newLanguage
    })

    watch(language, async (newLanguage) => {
      ready.value = false
      await registerLanguage(language.value)
      ready.value = true
    })

    const ready = ref(false)

    onMounted(async () => {
      await registerLanguage(language.value)
      ready.value = true
    })

    const highlightedCode = computed(() => {
      if (!ready.value) {
        return ''
      }

      if (!language.value) {
        const result = hljs.highlightAuto(props.code)
        return result.value
      }

      const result = hljs.highlight(props.code, { language: language.value })
      return result.value
    })

    const classes = computed(() => {
      if (!ready.value) {
        return ''
      }

      return `hljs language-${language.value}`

    })


    return () => h("div", { class: classes.value },
      h('pre', {},
        h('code', { innerHTML: highlightedCode.value }))
    );
  }

}

