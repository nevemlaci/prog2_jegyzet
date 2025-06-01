def define_env(env):
    @env.macro
    def run_button(link):
        return f'[ Futtasd! ](<{link}>){{ .md-button target="_blank" }}'