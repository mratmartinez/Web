use yew::{Component, Context, html, Html, Properties};

#[derive(PartialEq, Properties)]
pub struct Props;

pub struct PostList;

#[derive(Clone)]
struct PostListItem {
    title: String,
    summary: String,
    url: String
}

struct PostVector {
    posts: Vec<PostListItem>
}

impl Component for PostList {
    type Message = ();
    type Properties = Props;

    fn create(ctx: &Context<Self>) -> Self {
        PostList
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        let post = PostListItem {
            title: "Post Title".to_string(),
            summary: "This would be the summary.".to_string(),
            url: "/post-test".to_string()
        };
        
        let post_vector = PostVector {
            posts: Vec::from([post])
        };

        let the_post = post_vector.posts[0].clone();

        html! {
            <ul class="postlist">
                <li class="post postlist-item">
                    <a href={the_post.url}><h3>{the_post.title}</h3></a>
                    <p>{the_post.summary}</p>
                </li>
            </ul>
        }
    }
}