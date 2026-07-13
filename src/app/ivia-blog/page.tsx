export default function IviaBlogPage() {
  return (
    <main style={{ width: '100%', minHeight: '100vh' }}>
      <iframe
        src="/ivia-blog.html"
        style={{ width: '100%', height: '100vh', border: 'none' }}
        loading="lazy"
        title="IVIA Blog"
      />
    </main>
  );
}
