use yew::prelude::*;

#[function_component(App)]
pub fn app() -> Html {
    let header: Html = html! {
        <header>
            <div class="nav center">
                <div class="row">
                    <div class="col"><h1 class="nav-logo"><a href="/">{"Juancito"}</a></h1></div>
                    <div class="col"><a class="nav-item" href="/about">{"about"}</a></div>
                    <div class="col"><a class="nav-item" href="https://www.github.com/mratmartinez">{"git"}</a></div>
                </div>
            </div>
        </header>
    };

    html! {
        <main>
            {header}
            <p>{ "Test" }</p>
        </main>
    }
}
