        document.addEventListener('DOMContentLoaded', () => {
                const sidebar = document.querySelector('.sidebar');
                const contentContainer = document.querySelector('#main-content-inner');
                const loadingIndicator = document.querySelector('.loading-indicator');

                // Fecha todos os submenus, exceto o atual
                const closeOtherSubmenus = (currentSubmenu) => {
                    document.querySelectorAll('.submenu.show').forEach(submenu => {
                        if (submenu !== currentSubmenu) submenu.classList.remove('show');
                    });
                };

                // Exibe ou oculta o indicador de carregamento
                const toggleLoading = (show) => {
                    if (loadingIndicator) loadingIndicator.style.display = show ? 'block' : 'none';
                };

                // Adiciona ou atualiza os listeners de toggle de submenu
                const initSubmenuToggle = () => {
                    document.querySelectorAll('.toggle-submenu').forEach(icon => {
                        icon.removeEventListener('click', handleSubmenuClick);
                        icon.addEventListener('click', handleSubmenuClick);
                    });
                };

                // Handler de clique no toggle de submenu
                const handleSubmenuClick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();

                    const currentLi = e.currentTarget.closest('li');
                    const currentSubmenu = currentLi?.querySelector('.submenu');

                    if (!currentSubmenu) return;

                    const isOpen = currentSubmenu.classList.contains('show');
                    isOpen ? currentSubmenu.classList.remove('show') : (closeOtherSubmenus(currentSubmenu), currentSubmenu.classList.add('show'));
                };

                // Carrega conteúdo via AJAX
                const loadContent = (url, linkElement = null) => {
                    toggleLoading(true);
                    const parentSubmenu = linkElement?.closest('.submenu');

                    fetch(url)
                        .then(response => {
                            if (!response.ok) throw new Error('Network response was not ok');
                            return response.text();
                        })
                        .then(html => {
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            const newContent = doc.querySelector('#main-content-inner');
                            const newTitle = doc.querySelector('title')?.textContent;

                            if (newContent && contentContainer) {
                                contentContainer.innerHTML = newContent.innerHTML;
                                if (newTitle) document.title = newTitle;
                                history.pushState({ url }, '', url);

                                // Atualiza link ativo
                                sidebar.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
                                if (linkElement) linkElement.classList.add('active');

                                // Mantém submenu aberto se o link estava dentro de um
                                if (parentSubmenu) parentSubmenu.classList.add('show');

                                // Reativa toggle de submenu em conteúdo novo
                                initSubmenuToggle();
                            } else {
                                window.location.href = url;
                            }
                        })
                        .catch(() => window.location.href = url)
                        .finally(() => toggleLoading(false));
                };

                // Inicializa os toggles dos submenus
                initSubmenuToggle();

                // Adiciona evento a todos os links de navegação
                sidebar.querySelectorAll('a.nav-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        const href = link.getAttribute('href');
                        if (href === '#' || link.classList.contains('dropdown-toggle')) return;

                        e.preventDefault();
                        closeOtherSubmenus(link.closest('.submenu'));
                        loadContent(link.href, link);
                    });
                });

                // Suporte aos botões de voltar/avançar do navegador
                window.addEventListener('popstate', (e) => {
                    if (e.state?.url) {
                        loadContent(e.state.url);
                    } else {
                        location.reload();
                    }
                });

                // Carregamento inicial se não estiver na raiz
                if (window.location.pathname !== '/') {
                    const activeLink = sidebar.querySelector('.nav-link.active');
                    if (activeLink) loadContent(activeLink.href, activeLink);
                }

                // Adiciona evento ao botão de IA
                const aiButton = document.querySelector('.ai-chat-button');
                if (aiButton) {
                    aiButton.addEventListener('click', () => {
                        alert('Conversa com IA iniciada!'); // Substitua por sua implementação real
                    });
                }
            });
    