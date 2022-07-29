use yew::{Component, Context, html, Html, Properties};

#[derive(PartialEq, Properties)]
pub struct Props;

pub struct Post;

struct Post {
    title: String,
    summary: String,
    url: String
}

impl Component for Post {
    type Message = ();
    type Properties = Props;

    fn create(ctx: &Context<Self>) -> Self {
        Post
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        html! {
            <p>{"Test"}</p>
        }
    }
}