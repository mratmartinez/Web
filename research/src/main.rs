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

    let another_post = PostListItem {
        title: "Post Title 2".to_string(),
        summary: "This would be another summary.".to_string(),
        url: "/post-test-2".to_string()
    };    

    let post_vector = PostVector {
        posts: Vec::from([post, another_post])
    };

    for iter_post in post_vector.posts.iter() {
        let the_post = iter_post.clone();
        println!("{} / {} / {}", the_post.title, the_post.summary, the_post.url);
    }
}
