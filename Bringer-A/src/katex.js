import MarkdownIt from 'markdown-it';
import TexMathPlugin from 'markdown-it-texmath';
import Katex from 'katex';
import 'katex/dist/katex.css';
TexMathPlugin.use(Katex);
const DisableHtml = MarkdownIt({
	html: false,
	xhtmlOut: true,
	breaks: true,
	linkify: true,
	typographer: false,
	langPrefix: 'lang-',
	quotes: '“”‘’',
}).use(TexMathPlugin).use(require('markdown-it-highlightjs'));
const EnableHtml = MarkdownIt({
	html: true,
	xhtmlOut: true,
	breaks: true,
	linkify: true,
	typographer: false,
	langPrefix: 'lang-',
	quotes: '“”‘’',
}).use(TexMathPlugin) .use(require('markdown-it-highlightjs'));
export { DisableHtml, EnableHtml };
