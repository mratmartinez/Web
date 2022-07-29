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
        let the_post = PostListItem {
            title: "Post Title".to_string(),
            summary: "This would be the summary.".to_string(),
            url: "/post-test".to_string()
        };

        let another_post = PostListItem {
            title: "Another Title".to_string(),
            summary: "This would be another summary.".to_string(),
            url: "/post-test-2".to_string()
        };
        
        let post_vector = PostVector {
            posts: Vec::from([the_post, another_post])
        };

        let post_list = post_vector.posts.into_iter().map(|post| {
            html! {
                <li class="post postlist-item">
                    <a href={post.url}><h3>{post.title}</h3></a>
                    <p>{post.summary}</p>
                </li>
            }
        });

        html! {
            <ul class="postlist">
                {for post_list}
            </ul>
        }
    }
}