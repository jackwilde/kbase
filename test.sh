# Get version from source
current_version=$(cat VERSION)
current_major=$(cut -d '.' -f1-2 <<< "$current_version")

# Get details about last release
last_version=$(skopeo list-tags docker://ghcr.io/${{ github.repository_owner }}/${{ env.IMAGE_NAME }} | jq -r '[.Tags[] | select(. != "latest")] | sort | .[-1]')
last_major=$(cut -d '.' -f1-2 <<< "$last_version")
last_patch=$(cut -d '.' -f3 <<< "$last_version")

if [[ $current_major == "$last_major" ]]; then
  # Increment the patch version
  echo "increment"
  new_patch=$((++last_patch))
  echo "$new_patch"
  latest_version="${last_major}.${new_patch}"
else
  echo "Don't increment"
  # Reset the patch version to 1
  latest_version="${current_major}.1"
fi

echo "VERSION=$latest_version" >> $GITHUB_ENV