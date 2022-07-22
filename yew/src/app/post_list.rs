use yew::{Component, Context, html, Html, Properties};

#[derive(PartialEq, Properties)]
pub struct Props;

pub struct PostList;

struct PostListItem {
    title: String,
    summary: String,
    url: String
}

impl Component for PostList {
    type Message = ();
    type Properties = Props;

    fn create(ctx: &Context<Self>) -> Self {
        PostList
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        let title = "Post Title".to_string();
        let summary = "This would be the summary.".to_string();
        let url = "/post-test".to_string();

        let post = PostListItem {
            title: title,
            summary: summary,
            url: url
        };

        html! {
            <ul class="postlist">
                <li class="post postlist-item">
                    <a href={post.url}><h3>{post.title}</h3></a>
                    <p>{post.summary}</p>
                </li>
            </ul>
        }
    }
}