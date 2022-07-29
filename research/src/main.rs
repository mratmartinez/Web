fn main() {
    #[derive(Clone)]
    struct PostListItem {
        title: String,
        summary: String,
        url: String
        }

    struct PostVector {
        posts: Vec<PostListItem>
    }

    let post = PostListItem {
        title: "Post Title".to_string(),
        summary: "This would be the summary.".to_string(),
        url: "/post-test".to_string()
    };
    
    let post_vector = PostVector {
        posts: Vec::from([post])
    };

    let the_post = post_vector.posts[0].clone();

    println!("{} / {} / {}", the_post.title, the_post.summary, the_post.url);
}
