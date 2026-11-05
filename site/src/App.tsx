import { For, Show, createSignal } from "solid-js";
import { catalog, mediaUrl, type Animation } from "./catalog";
import styles from "./App.module.css";

function Tile(props: { item: Animation; onOpen: (item: Animation) => void }) {
  return (
    <button class={styles.tile} onClick={() => props.onOpen(props.item)}>
      <img
        class={styles.poster}
        src={mediaUrl(props.item.poster)}
        alt=""
        loading="lazy"
      />
      <span class={styles.overlay}>
        <span class={styles.tileTitle}>{props.item.title}</span>
        <span class={styles.tileMeta}>{props.item.seconds} s</span>
      </span>
    </button>
  );
}

function Viewer(props: { item: Animation; onClose: () => void }) {
  return (
    <div class={styles.backdrop} onClick={props.onClose}>
      <article
        class={styles.viewer}
        role="dialog"
        aria-label={props.item.title}
        onClick={(event) => event.stopPropagation()}
      >
        <video
          class={styles.video}
          src={mediaUrl(props.item.video)}
          poster={mediaUrl(props.item.poster)}
          controls
          autoplay
          loop
          playsinline
        />
        <div class={styles.caption}>
          <p class={styles.topic}>{props.item.topic}</p>
          <h2 class={styles.captionTitle}>{props.item.title}</h2>
          <p class={styles.summary}>{props.item.summary}</p>
          <button class={styles.close} onClick={props.onClose}>
            Cerrar
          </button>
        </div>
      </article>
    </div>
  );
}

export function App() {
  const [open, setOpen] = createSignal<Animation | null>(null);

  return (
    <main class={styles.page}>
      <header class={styles.header}>
        <h1 class={styles.brand}>CAE Física</h1>
        <p class={styles.tagline}>
          Animaciones de física hechas con código. Una idea por video.
        </p>
        <p class={styles.count}>{catalog.length} animaciones</p>
      </header>
      <section class={styles.grid} aria-label="Animaciones">
        <For each={catalog}>
          {(item) => <Tile item={item} onOpen={setOpen} />}
        </For>
      </section>
      <Show when={open()}>
        {(item) => <Viewer item={item()} onClose={() => setOpen(null)} />}
      </Show>
    </main>
  );
}
